from django.db.models import QuerySet


class TransactionQuerySet(QuerySet):
    """Кастомный QuerySet для управления запросами транзакций."""

    def with_related(self):
        """Оптимизирует запрос, предвыбирая связанные сущности."""
        return self.select_related(
            'status',
            'transaction_type',
            'category',
            'subcategory',
        )
