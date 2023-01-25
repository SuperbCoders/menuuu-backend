"""
Настройки встроенной админки Django для управления тарифами
"""

from django.contrib import admin
from parler.admin import TranslatableAdmin

from tariffs.models import Tariff


@admin.register(Tariff)
class TariffAdmin(TranslatableAdmin):
    list_display = ('name', 'month_price', 'year_price')
    search_fields = ('name', )
    fields = (
        ('name', 'description'),
        ('month_price', 'year_price')
    )
