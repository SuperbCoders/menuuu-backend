#! /usr/bin/env bash

# Ожидает запуска СУБД в течении 5 секунд
# Применяет миграции базы данных (будет иметь эффект только при первом запуске)
# Запускает сервер приложений gunicorn на порту 8000
sleep 5 && python manage.py migrate && gunicorn menu_backend.wsgi:application --bind 0.0.0.0:8000
