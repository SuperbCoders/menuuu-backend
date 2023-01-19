"""
Настройки встроенной админки Django для ресторанов
"""

from parler.admin import TranslatableAdmin
from django.contrib import admin

from restaurants.models import Restaurant, RestaurantStaff, RestaurantCategory


@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(TranslatableAdmin):
    list_display = ['name']


@admin.register(Restaurant)
class RestaurantAdmin(TranslatableAdmin):
    list_display = ['name', 'stars']


@admin.register(RestaurantStaff)
class RestaurantStaffAdmin(TranslatableAdmin):
    list_display = ['restaurant', 'user']
