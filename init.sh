#!/bin/sh

set -e

echo "Запуск миграций"
python manage.py migrate --noinput

echo "Собираем статику"
python manage.py collectstatic --noinput

echo "Загрузка моковых данных"
python manage.py load_mock_data

echo "Проект готов!"