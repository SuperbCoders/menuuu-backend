"""
Модели данных для ресторанов и персонала ресторанов
---------------------------------------------------

Содержит следующие модели данных.

*   Категория ресторанов
*   Ресторан
*   Сотрудник или владелец ресторана
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields

from users.models import User


class RestaurantCategory(TranslatableModel):
    """
    Категория ресторанов
    --------------------
    """
    class Meta:
        db_table = 'restaurants_restaurantcategory'
        ordering = ['-stars', 'pk']
        verbose_name = _('restaurant category')
        verbose_name_plural = _('restaurant categories')

    translations = TranslatedFields(
        name=models.CharField(
            max_length=100,
            verbose_name=_("Category name"),
            blank=False, null=False
        )
    )
    stars = models.PositiveSmallIntegerField(
        default=0, blank=False, null=False
    )


class Restaurant(TranslatableModel):
    """
    Ресторан
    --------
    """
    class Meta:
        db_table = 'restaurants_restaurant'
        # Сортировка по имени в модели невозможна, если имя зависит от языка
        ordering = ['pk']
        verbose_name = _('restaurant')
        verbose_name_plural = _('restaurants')

    translations = TranslatedFields(
        name=models.CharField(
            max_length=100,
            verbose_name=_("Restaurant name"),
            blank=False, null=False
        ),
        description=models.TextField(
            max_length=5000,
            verbose_name=_("Restaurant description"),
            blank=True, null=False
        )
    )

    longitude = models.DecimalField(
        max_digits=20, decimal_places=15,
        blank=True, null=True,
        verbose_name=_('Longitude')
    )
    latitude = models.DecimalField(
        max_digits=20, decimal_places=15,
        blank=True, null=True,
        verbose_name=_('Latitude')
    )

    def __str__(self):
        return self.name


class RestaurantStaff(models.Model):
    """
    Владелец или сотрудник ресторана
    """

    POSITION_CHOICES = [
        ('owner', _('Restaurant owner')),
        ('worker', _('Restaurant worker')),
    ]

    class Meta:
        ordering = ['pk']
        db_table = 'restaurants_restaurantstaff'
        verbose_name = _('restaurant ownership or employment')
        verbose_name = _('restaurant ownerships or employments')

    user = models.ForeignKey(
        to=User,
        verbose_name=_('User'),
        related_name='restaurant_staff',
        on_delete=models.CASCADE,
        blank=False, null=False
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        verbose_name=_('Restaurant'),
        related_name='restaurant_staff',
        on_delete=models.CASCADE,
        blank=False, null=False
    )
    position = models.CharField(
        max_length=25,
        verbose_name=_('Position'),
        choices=POSITION_CHOICES,
        blank=False, null=False
    )

    def __str__(self):
        return f"User {self.user.username} in {self.restaurant.name}"
