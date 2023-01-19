"""
Настройки встроенной админки Django для меню и блюд
"""

from django.contrib import admin
from parler.admin import TranslatableAdmin

from menus.models import Menu, MenuSection, MenuCourse


@admin.register(MenuCourse)
class MenuCourseAdmin(TranslatableAdmin):
    """
    Настройки админки Django для блюд
    """
    list_display = ('title', 'price')
    search_fields = ('title', )
    fields = (
        # Название блюда и его состав
        ('title', 'composition'),
        # Цена и время приготовления
        ('price', 'cooking_time'),
        # Доступно для посетителей
        ('published', ),
        # Прочие опции
        ('options', )
    )
