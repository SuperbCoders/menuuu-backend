FROM python:3.10
WORKDIR /menu_backend
COPY requirements.txt /menu_backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . /menu_backend/

# Собрать все статические файлы в папку откуда Nginx будет отдавать
# их напрямую
RUN python manage.py collectstatic --no-input

# Запуск сервера скриптом, который применит миграции при необходимости
# прежде чем фактически запускать сервер
RUN chmod u+x /menu_backend/entrypoint.sh
CMD ["/menu_backend/entrypoint.sh"]
