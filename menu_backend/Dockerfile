FROM python:3.10
WORKDIR /menu_backend
COPY requirements.txt /menu_backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . /menu_backend/
RUN python manage.py collectstatic --no-input
RUN chmod u+x /menu_backend/start.sh
# Запуск сервера скриптом, который применит миграции при необходимости
# прежде чем фактически запускать сервер
CMD ["./start.sh"]
