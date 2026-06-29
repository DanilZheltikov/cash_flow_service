from django.views.generic import (
    CreateView,
    DeleteView,
    TemplateView,
    UpdateView,
)

from ..models import Category, Subcategory, TransactionStatus, TransactionType
from ..mixins import DirectoriesMixin


class DirectoryManager(TemplateView):
    """Главная страница управления всеми справочниками системы."""

    template_name = 'directories/directories.html'

    def get_context_data(self, **kwargs):
        """Добавляет в контекст данные всех справочников."""
        context = super().get_context_data(**kwargs)

        context['statuses'] = TransactionStatus.objects.all()
        context['types'] = TransactionType.objects.all()
        context['categories'] = (
            Category.objects.select_related('transaction_type').all()
        )
        context['subcategories'] = (
            Subcategory.objects.select_related(
                'category',
                'category__transaction_type'
            ).all()
        )
        return context


class DirectoryCreateView(DirectoriesMixin, CreateView):
    """Универсальное представление для создания записи справочника."""

    title = 'Создание'
    mode = 'create'


class DirectoryUpdateView(DirectoriesMixin, UpdateView):
    """Универсальное представление для редактирования записи справочника."""

    title = 'Редактирование'
    mode = 'update'


class DirectoryDeleteView(DirectoriesMixin, DeleteView):
    """Универсальное представление для удаления записи справочника."""

    title = 'Удаление'
    mode = 'delete'
