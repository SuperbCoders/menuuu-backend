from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields


class Tariff(TranslatableModel):
    """
    Тариф для ресторанов
    """
    class Meta:
        db_table = 'tariffs_tariff'
        ordering = ['pk']
        verbose_name = _('tariff')
        verbose_name_plural = _('tariff')

    translations = TranslatedFields(
        name=models.CharField(
            max_length=250,
            verbose_name=_("Name"),
            blank=False, null=False
        ),
        description=models.TextField(
            max_length=5000,
            verbose_name=_("Description"),
            blank=True, null=False
        )
    )
    month_price = models.IntegerField(
        verbose_name=_("Price per month"),
        blank=False, null=False
    )
    year_price = models.IntegerField(
        verbose_name=_("Price per year"),
        blank=False, null=False
    )

    def __str__(self):
        return self.name
