from django.urls import path

from .views.transaction import (
    IndexView,
    TransactionCreateView,
    TransactionDetailView,
    TransactionDeleteView,
    TransactionUpdateView
)

app_name = 'transaction'

urlpatterns = [
    path(
        'transactions/create/',
        TransactionCreateView.as_view(),
        name='create_transaction'
    ),
    path(
        'transactions/<int:transaction_id>/',
        TransactionDetailView.as_view(),
        name='transaction_detail'
    ),
    path(
        'transactions/<int:transaction_id>/edit/',
        TransactionUpdateView.as_view(),
        name='edit_transaction'
    ),
    path(
        'transactions/<int:transaction_id>/delete/',
        TransactionDeleteView.as_view(),
        name='delete_transaction'
    ),
    path('', IndexView.as_view(), name='index'),
]
