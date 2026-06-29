from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey

from cash_flow_service.constants import (
    DECIMAL_PLACES,
    MAX_DIGITS,
    MAX_LEN_COMMENT,
    MAX_LEN_NAME,
    MIN_AMOUNT_VALUE
)


class TransactionStatus(models.Model):
    """Справочник статусов ДДС (Бизнес, Личное, Налог)."""

    name = models.CharField(
        'Статус',
        max_length=MAX_LEN_NAME,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    """Справочник типов транзакций (Пополнение, Списание)."""

    name = models.CharField(
        'Тип',
        max_length=MAX_LEN_NAME,
        unique=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Справочник категорий транзакций."""

    name = models.CharField(
        'Категория',
        max_length=MAX_LEN_NAME,
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        verbose_name='Тип транзакции',
        on_delete=models.CASCADE,
        related_name='categories',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'transaction_type'],
                name='unique_category_name_transaction_type'
            )
        ]

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Справочник подкатегорий транзакций."""

    name = models.CharField(
        'Подкатегория',
        max_length=MAX_LEN_NAME,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Название категории',
        on_delete=models.CASCADE,
        related_name='subcategories',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'category'],
                name='unique_subcategory_name_category'
            )
        ]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Модель учета движения денежных средств (ДДС)."""

    amount = models.DecimalField(
        'Сумма',
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        validators=[
            MinValueValidator(Decimal(MIN_AMOUNT_VALUE))
        ]
    )
    created_at = models.DateField(
        'Дата создания',
        default=timezone.now,
        db_index=True,
    )
    comment = models.TextField(
        'Комментарий',
        max_length=MAX_LEN_COMMENT,
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        TransactionStatus,
        verbose_name='Статус транзакции',
        on_delete=models.PROTECT,
    )
    transaction_type = models.ForeignKey(
        TransactionType,
        verbose_name='Тип транзакции',
        on_delete=models.PROTECT,
    )
    category = ChainedForeignKey(
        Category,
        chained_field='transaction_type',
        chained_model_field='transaction_type',
        show_all=False,
        auto_choose=True,
        verbose_name='Категория транзакции',
        on_delete=models.PROTECT,
    )
    subcategory = ChainedForeignKey(
        Subcategory,
        chained_field='category',
        chained_model_field='category',
        show_all=False,
        auto_choose=True,
        verbose_name='Подкатегория транзакции',
        on_delete=models.PROTECT,
    )

    class Meta:
        default_related_name = 'transactions'
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']

    def __str__(self):
        return (
            f'{self.transaction_type.name} '
            f'{self.created_at} на {self.amount} руб.'
        )

    def get_absolute_url(self):
        """Возвращает URL-адрес страницы детального просмотра записи."""
        return reverse(
            'transaction:transaction_detail',
            kwargs={'transaction_id': self.pk}
        )
