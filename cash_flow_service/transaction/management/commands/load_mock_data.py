import sys

from django.core.management import BaseCommand

from transaction.models import (
    Category,
    Subcategory,
    TransactionStatus,
    TransactionType
)


class Command(BaseCommand):

    help = 'Загружает моковые данные в базу'

    def handle(self, *args, **options):
        try:
            TransactionStatus.objects.bulk_create(
                objs=(
                    TransactionStatus(name='Бизнес'),
                    TransactionStatus(name='Личное'),
                    TransactionStatus(name='Налог'),
                )
            )
            transaction_types = TransactionType.objects.bulk_create(
                objs=(
                    TransactionType(name='Пополнение'),
                    TransactionType(name='Списание'),
                )
            )
            categories = Category.objects.bulk_create(
                objs=(
                    Category(
                        name='Инфраструктура',
                        transaction_type=transaction_types[1]
                    ),
                    Category(
                        name='Маркетинг',
                        transaction_type=transaction_types[1]
                    )
                )
            )
            Subcategory.objects.bulk_create(
                objs=(
                    Subcategory(name='VPS', category=categories[0]),
                    Subcategory(name='Proxy', category=categories[0]),
                    Subcategory(name='Farpost', category=categories[1]),
                    Subcategory(name='Avito', category=categories[1]),
                )
            )
            self.stdout.write(self.style.SUCCESS('Моковые данные загружены'))

        except Exception as e:
            self.stderr.write(f'Ошибка записи в бд {e}')
            sys.exit(1)
