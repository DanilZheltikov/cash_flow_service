from django_filters import DateFromToRangeFilter, FilterSet
from django_filters.widgets import RangeWidget

from .models import Transaction


class TransactionFilter(FilterSet):
    """Фильтр для записей ДДС по периоду и справочникам."""

    date = DateFromToRangeFilter(
        field_name='created_at',
        label='Период',
        widget=RangeWidget(
            attrs={'type': 'date'}
        )
    )

    class Meta:
        model = Transaction
        fields = {
            'status': ['exact'],
            'transaction_type': ['exact'],
            'category': ['exact'],
            'subcategory': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
