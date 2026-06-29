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
from ..mixins import TransactionBaseMixin, WithRelatedMixin
from ..models import Transaction
from cash_flow_service.constants import TRANSACTION_COUNT


class IndexView(WithRelatedMixin, FilterView):
    """Главная страница со списком записей ДДС и фильтрацией."""

    model = Transaction
    template_name = 'transaction/index.html'
    paginate_by = TRANSACTION_COUNT
    filterset_class = TransactionFilter


class TransactionDetailView(WithRelatedMixin, DetailView):
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
