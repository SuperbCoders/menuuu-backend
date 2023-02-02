"""
Модуль управления пользователями
--------------------------------
"""

import os

from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError


class UsersConfig(AppConfig):
    """
    Настройки модуля управления пользователями
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        Инициализация модуля работы с пользователями
        --------------------------------------------

        Если в системе нет пользователя администратора, то создать его, взяв имя,
        адрес электронной почты и пароль из переменных окружения ADMIN_USERNAME,
        ADMIN_EMAIL и ADMIN_PASSWORD. По умолчанию имя и пароль admin, электронный
        адрес admin@localhost.
        """
        super().ready()
        from users.models import User
        try:
            if not User.objects.filter(is_active=True, is_staff=True).exists():
                User.objects.create_superuser(
                    username=os.getenv("ADMIN_USERNAME", "admin"),
                    password=os.getenv("ADMIN_PASSWORD", "admin"),
                    email=os.getenv("ADMIN_EMAIL", "admin@localhost"),
                    phone=os.getenv("ADMIN_PHONE", '')
                )
        except (OperationalError, ProgrammingError):
            # В процессе начального создания базы таблицы пользователей еще нет,
            # поэтому игнорируем ошибку и откладываем создание пользователя до
            # следующего запуска
            pass
