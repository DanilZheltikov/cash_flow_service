from django.urls import path

from . import views

app_name = 'transaction'

urlpatterns = [
    path(
        'transactions/create/',
        views.TransactionCreateView.as_view(),
        name='create_transaction'
    ),
    path(
        'transactions/<int:transaction_id>/',
        views.TransactionDetailView.as_view(),
        name='transaction_detail'
    ),
    path(
        'transactions/<int:transaction_id>/edit/',
        views.TransactionUpdateView.as_view(),
        name='edit_transaction'
    ),
    path(
        'transactions/<int:transaction_id>/delete/',
        views.TransactionDeleteView.as_view(),
        name='delete_transaction'
    ),
    path('', views.IndexView.as_view(), name='index'),
]
