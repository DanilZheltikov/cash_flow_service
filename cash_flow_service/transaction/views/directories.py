from typing import Literal

from django.contrib import messages
from django.db.models import ProtectedError
from django.db.utils import IntegrityError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from ..models import Category, Subcategory, TransactionStatus, TransactionType

DIRECTORY_MODELS_MAP = {
    'status': TransactionStatus,
    'type': TransactionType,
    'category': Category,
    'subcategory': Subcategory
}
MODEL_TYPE = Literal['status', 'type', 'category', 'subcategory']


class DirectoryManager(TemplateView):
    """Главная страница управления всеми справочниками системы."""

    template_name = 'directories/directories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['statuses'] = TransactionStatus.objects.all()
        context['types'] = TransactionType.objects.all()
        context['categories'] = (
            Category.objects.select_related('transaction_type').all()
        )
        context['subcategories'] = (
            Subcategory.objects.select_related('category').all()
        )
        return context


@require_POST
def manage_directory_item(
    request: HttpRequest,
    model_type: MODEL_TYPE,
    item_id: int | None = None
):
    """Создание и редактирование элементов справочников."""
    model = DIRECTORY_MODELS_MAP.get(model_type)

    if not model:
        return redirect('directory-management')

    name = request.POST.get('name', '').strip()

    if not name:
        messages.error(
            request,
            'Название элемента не может быть пустым.'
        )
        return redirect('directory-management')

    instance = get_object_or_404(model, id=item_id) if item_id else model()
    instance.name = name

    if model_type == 'category':
        type_id = request.POST.get('transaction_type')

        if not type_id:
            messages.error(request, 'Необходимо выбрать тип транзакции.')
            return redirect('directory-management')

        instance.transaction_type_id = int(type_id)

    if model_type == 'subcategory':
        category_id = request.POST.get('category')

        if not category_id:
            messages.error(
                request,
                'Необходимо выбрать родительскую категорию.'
            )
            return redirect('directory-management')

        instance.category_id = int(category_id)

    try:
        instance.save()
        messages.success(request, f'Элемент {name} успешно сохранен.')

    except IntegrityError:
        messages.error(
            request,
            'Ошибка уникальности! Такой элемент уже существует в этой группе.'
        )

    return redirect('directory-management')


@require_POST
def delete_directory_item(
    request: HttpRequest,
    model_type: MODEL_TYPE,
    item_id: int
):
    """Удаление элементов справочников."""
    model = DIRECTORY_MODELS_MAP.get(model_type)

    if not model:
        return redirect('directory-management')

    instance = get_object_or_404(model, id=item_id)

    try:
        instance.delete()
        messages.success(request, f'Элемент {instance.name} успешно удален.')

    except ProtectedError:
        messages.error(
            request,
            f'Невозможно удалить {instance.name}, '
            'так как он используется в существующих транзакциях.'
        )
