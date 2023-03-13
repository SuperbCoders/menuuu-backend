"""
Настройки встроенной админки Django для ресторанов
"""

from django.contrib import admin
from parler.admin import TranslatableAdmin

from restaurants.models import Restaurant, RestaurantStaff, RestaurantCategory


@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(TranslatableAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Restaurant)
class RestaurantAdmin(TranslatableAdmin):
    list_display = ('name', 'stars')
    search_fields = ('name', 'phone')
    fields = (
        # Основные сведения
        ('name', 'phone', 'site', 'category', 'stars'),
        # Описание
        ('description', ),
        # Изображения
        ('logo', 'picture'),
        # Адрес
        ('country', 'city', 'street', 'building', 'address_details', 'zip_code'),
        # Координаты
        ('longitude', 'latitude')
    )


@admin.register(RestaurantStaff)
class RestaurantStaffAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user')
    search_fields = ('restaurant__name', 'user__username')
