from django.contrib import admin

from .models import (
    Category,
    Subcategory,
    Transaction,
    TransactionStatus,
    TransactionType
)


class BaseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'created_at',
        'status',
        'transaction_type',
        'category',
        'subcategory',
        'amount'
    ]
    search_fields = [
        'category__name',
        'status__name',
        'subcategory__name',
        'transaction_type__name'
    ]
    list_filter = ['created_at']


@admin.register(TransactionStatus)
class TransactionStatusAdmin(BaseAdmin):
    pass


@admin.register(TransactionType)
class TransactionTypeAdmin(BaseAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = [*BaseAdmin.list_display, 'transaction_type']


@admin.register(Subcategory)
class SubcategoryAdmin(BaseAdmin):
    list_display = [*BaseAdmin.list_display, 'category']
