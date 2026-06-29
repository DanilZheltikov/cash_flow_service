from django import forms

from cash_flow_service.constants import DATE_FORMAT, TEXT_AREA_ROWS

from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            'status',
            'transaction_type',
            'category',
            'subcategory',
            'created_at',
            'amount',
            'comment'
        ]
        widgets = {
            'created_at': forms.DateInput(
                attrs={'type': 'date'},
                format=DATE_FORMAT
            ),
            'comment': forms.Textarea(
                attrs={'rows': TEXT_AREA_ROWS}
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if (
            category
            and transaction_type
            and category.transaction_type_id != transaction_type.id
        ):
            self.add_error(
                field='category',
                error=(
                    f'{category.name} '
                    f'не относится к типу {transaction_type.name}'
                )
            )

        if subcategory and category and subcategory.category_id != category.id:
            self.add_error(
                field='subcategory',
                error=(
                    f'{subcategory.name} '
                    f'не связана с категорией {category.name}'
                )
            )

        return cleaned_data
