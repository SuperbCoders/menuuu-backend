"""
Настройки админки Django для работы с пользователями
"""

from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    """
    Настройки админки для модели пользователей
    """
    list_display = ('username', 'email', 'phone')
    readonly_fields = ('date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name')
    fields = (
        # Имя пользователя и контакты
        ('username', 'email', 'phone'),
        # Полное имя
        ('last_name', 'first_name'),
        # Полномочия в системе
        ('is_active', 'is_staff', 'is_superuser'),
        # Прочие сведения
        ('date_joined', 'last_login')
    )


admin.site.register(User, UserAdmin)
