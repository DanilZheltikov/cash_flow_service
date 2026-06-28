from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView
)
from django_filters.views import FilterView

from ..forms import TransactionForm
from ..filters import TransactionFilter
from ..mixins import TransactionBaseMixin
from ..models import Transaction
from cash_flow_service.constants import TRANSACTION_COUNT


class IndexView(FilterView):
    """Главная страница со списком записей ДДС и фильтрацией."""

    model = Transaction
    template_name = 'transaction/index.html'
    paginate_by = TRANSACTION_COUNT
    filterset_class = TransactionFilter

    def get_queryset(self):
        """Оптимизирует запросы к БД, подгружая связанные справочники."""
        return super().get_queryset().select_related(
            'status', 'transaction_type', 'category', 'subcategory'
        )


class TransactionDetailView(DetailView):
    """Страница детального просмотра отдельной записи ДДС."""

    model = Transaction
    pk_url_kwarg = 'transaction_id'
    template_name = 'transaction/detail.html'


class TransactionUpdateView(TransactionBaseMixin, UpdateView):
    """Представление для изменения записи ДДС с редиректом на detail."""

    title = 'Редактирование'
    mode = 'update'
    form_class = TransactionForm


class TransactionDeleteView(TransactionBaseMixin, DeleteView):
    """Представление для удаления записи ДДС с редиректом на index."""

    title = 'Удаление'
    mode = 'delete'
    success_url = reverse_lazy('index')


class TransactionCreateView(TransactionBaseMixin, CreateView):
    """Представление для создания новой записи ДДС с редиректом на detail."""

    title = 'Создание'
    mode = 'create'
    form_class = TransactionForm
