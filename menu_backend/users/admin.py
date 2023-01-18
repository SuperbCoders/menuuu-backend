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
        ('username', 'email', 'phone'),
        ('last_name', 'first_name'),
        ('is_active', 'is_staff', 'is_superuser'),
        ('date_joined', 'last_login')
    )


admin.site.register(User, UserAdmin)
