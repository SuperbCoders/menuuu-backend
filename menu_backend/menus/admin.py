"""
Настройки встроенной админки Django для меню и блюд
"""

from django.contrib import admin
from parler.admin import (
    TranslatableAdmin,
    TranslatableTabularInline,
    TranslatableStackedInline
)

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
        # В каком меню, в каком разделе, доступно ли для посетителей
        ('menu', 'section', 'published'),
        # Прочие опции
        ('options', ),
    )


class MenuCourseInline(TranslatableStackedInline):
    """
    Форма редактирования блюд встроенная в форму редактирования раздела меню
    """
    model = MenuCourse
    fields = (
        ('title', 'section'),
        ('cooking_time', 'price', 'published'),
        ('composition', ),
        ('options', )
    )


class MenuSectionInline(TranslatableTabularInline):
    """
    Форма редактирования раздела меню встроенная в форму редактирования меню
    """
    model = MenuSection
    fields = ('title', )


@admin.register(Menu)
class MenuAdmin(TranslatableAdmin):
    list_display = ('title', 'restaurant')
    fields = ('title', 'restaurant', 'published')
    inlines = (MenuSectionInline, MenuCourseInline)
