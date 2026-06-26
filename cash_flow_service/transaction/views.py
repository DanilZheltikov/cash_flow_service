from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView
)
from django_filters.views import FilterView

from .forms import TransactionForm
from .filters import TransactionFilter
from .mixins import TransactionBaseMixin
from .models import Transaction
from cash_flow_service.constants import TRANSACTION_COUNT


class IndexView(FilterView):
    model = Transaction
    template_name = 'transaction/index.html'
    paginate_by = TRANSACTION_COUNT
    filterset_class = TransactionFilter

    def get_queryset(self):
        return super().get_queryset().select_related(
            'status', 'transaction_type', 'category', 'subcategory'
        )


class TransactionDetailView(DetailView):
    model = Transaction
    pk_url_kwarg = 'transaction_pk'
    template_name = 'transaction/detail.html'


class TransactionUpdateView(TransactionBaseMixin, UpdateView):

    form_class = TransactionForm


class TransactionDeleteView(TransactionBaseMixin, DeleteView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TransactionForm(instance=self.object)
        return context


class TransactionCreateView(TransactionBaseMixin, CreateView):

    form_class = TransactionForm
