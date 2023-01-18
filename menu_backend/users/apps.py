"""
Модуль управления пользователями
--------------------------------
"""

from django.apps import AppConfig


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
        if not User.objects.filter(is_active=True, is_staff=True).exists():
            User.objects.create_superuser(
                username=os.getenv("ADMIN_USERNAME", "admin"),
                password=os.getenv("ADMIN_PASSWORD", "admin"),
                email=os.getenv("ADMIN_EMAILs", "admin@localhost"),
            )
