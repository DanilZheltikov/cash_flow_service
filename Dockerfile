FROM python:3.12

WORKDIR /app

RUN pip install gunicorn==23.0.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x init.sh

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cash_flow_service.wsgi:application"]