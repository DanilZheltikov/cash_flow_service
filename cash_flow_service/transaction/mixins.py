from .models import Transaction


class TransactionBaseMixin:
    model = Transaction
    pk_url_kwarg = 'transaction_id'
    template_name = 'transaction/create.html'
