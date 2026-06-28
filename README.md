# cash_flow_service
 Веб-сервис для управления движением денежных средств

ДДС (движение денежных средств) — это процесс учета, управления и анализа
поступлений и списаний денежных средств компании или частного лица.

## Запуск проекта:

1. Клонируйте репозиторий:

```bash
git clone https://github.com/DanilZheltikov/cash_flow_service.git
```
2. Перейдите в директорию проекта:

```bash
cd cash_flow_service

```

3. Создайте и активируйте виртуальное окружение:

```bash
# Windows:
python -m venv venv
source venv/Scripts/activate

# Linux / Mac:
python3 -m venv venv
source venv/bin/activate
```

4. Установите зависимости:

```bash
pip install -r requirements.txt
```

5. Создайте и заполните в директории проекта файл `.env`:

```env
SECRET_KEY=your-super-secret-key
```

6. Выполните миграции:

```bash
python manage.py migrate
```

7. Загрузите моковые данные:

```bash
python manage.py load_mock_data
```

8. Запустите сервер разработки:

```bash
python manage.py runserver
```

## Скриншоты:

### Главная:
![index](screenshots/index.png)

### Страница справочников:
![directories](screenshots/directories.png)

### Страница с формами:

![formpage](screenshots/formpage.png)


## :man_technologist: Автор

* [Danil Zheltikov](https://github.com/DanilZheltikov)