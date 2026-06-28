from django.urls import path

from .views.directories import (
    DirectoryCreateView,
    DirectoryDeleteView,
    DirectoryManager,
    DirectoryUpdateView
)
from .views.transaction import (
    IndexView,
    TransactionCreateView,
    TransactionDetailView,
    TransactionDeleteView,
    TransactionUpdateView
)

app_name = 'transaction'

urlpatterns = [
    # Транзакции:
    path('', IndexView.as_view(), name='index'),
    path(
        'create/',
        TransactionCreateView.as_view(),
        name='create_transaction'
    ),
    path(
        '<int:transaction_id>/',
        TransactionDetailView.as_view(),
        name='transaction_detail'
    ),
    path(
        '<int:transaction_id>/edit/',
        TransactionUpdateView.as_view(),
        name='edit_transaction'
    ),
    path(
        '<int:transaction_id>/delete/',
        TransactionDeleteView.as_view(),
        name='delete_transaction'
    ),

    # Справочники:
    path(
        'directories/',
        DirectoryManager.as_view(),
        name='directory-management'
    ),
    path(
        'directories/add/<str:model_type>/',
        DirectoryCreateView.as_view(),
        name='directory-add'
    ),
    path(
        'directories/edit/<str:model_type>/<int:item_id>/',
        DirectoryUpdateView.as_view(),
        name='directory-edit'
    ),
    path(
        'directories/delete/<str:model_type>/<int:item_id>/',
        DirectoryDeleteView.as_view(),
        name='directory-delete'
    ),
]
