from http import HTTPStatus

from django.shortcuts import render


def error_handler(request, reason='', exception=None):
    """Универсальный хендлер для ошибок"""
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    if exception:
        status_code = getattr(exception, 'status_code', HTTPStatus.NOT_FOUND)

    context = {
        'status_code': status_code,
        'message': get_error_message(status_code)
    }

    return render(request, 'error.html', context, status=status_code)


def get_error_message(status_code):
    """Отдает сообщение ошибки по статус коду."""
    messages = {
        400: 'Некорректный запрос.',
        403: 'Доступ запрещен.',
        404: 'Страница не найдена.',
        500: 'Ошибка сервера. Мы уже чиним.'
    }
    return messages.get(status_code, 'Что-то пошло не так.')
