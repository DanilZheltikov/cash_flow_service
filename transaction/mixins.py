from typing import Any, Type

from django.forms import ModelForm, modelform_factory
from django.http import Http404
from django.db.models import Model, QuerySet
from django.urls import reverse_lazy

from .models import (
    Category,
    Subcategory,
    Transaction,
    TransactionStatus,
    TransactionType
)


class WithRelatedMixin:
    """Оптимизирует запросы к БД, подгружая связанные справочники."""
    def get_queryset(self):
        return super().get_queryset().with_related()


class CrudContextMixin:
    """Миксин для добавления режима и заголовка в контекст шаблона."""

    title: str | None = None
    mode: str | None = None

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляет переменные 'mode' и 'title' в контекст."""
        context = super().get_context_data(**kwargs)
        context['mode'] = self.mode
        context['title'] = self.title
        return context


class TransactionBaseMixin(WithRelatedMixin, CrudContextMixin):
    """Базовый миксин для CRUD-представлений транзакций."""

    model: Type[Model] = Transaction
    pk_url_kwarg: str = 'transaction_id'
    template_name: str = 'transaction/CRUD.html'


class DirectoriesCreateUpdateMixin:
    """Миксин для автоматической генерации формы модели."""

    def get_form_class(self) -> Type[ModelForm]:
        """Возвращает класс формы со всеми полями модели."""
        return modelform_factory(
            self.get_model(),
            fields='__all__'
        )


class DirectoriesMixin(DirectoriesCreateUpdateMixin, CrudContextMixin):
    """Миксин для динамической работы со справочниками системы."""

    directories: dict[str, Type[Model]] = {
        'status': TransactionStatus,
        'type': TransactionType,
        'category': Category,
        'subcategory': Subcategory,
    }
    template_name: str = 'directories/CRUD.html'
    pk_url_kwarg: str = 'item_id'
    success_url: str = reverse_lazy('transaction:directory-management')

    def get_model(self) -> Type[Model]:
        """Возвращает класс модели на основе URL-параметра model_type."""
        model = self.directories.get(self.kwargs['model_type'])

        if not model:
            raise Http404

        return model

    def get_queryset(self) -> QuerySet[Any]:
        """Возвращает набор всех записей для динамической модели."""
        return self.get_model().objects.all()
