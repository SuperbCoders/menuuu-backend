"""
Модели данных для меню и блюд
-----------------------------

Включает следующие модели данных

*   Меню
*   Раздел меню
*   Блюдо
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields

from restaurants.models import Restaurant


class Menu(TranslatableModel):
    """
    Меню
    ----

    Меню ресторана имеет общий заголовок, флаг активности, ссылку не ресторан.
    """
    class Meta:
        db_table = 'menus_menu'
        # Сортировка по заголовку невозможна, если заголовок зависит от языка
        ordering = ['pk']
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    translations = TranslatedFields(
        title=models.CharField(
            max_length=250,
            verbose_name=_("Title"),
            blank=False, null=False
        ),
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.SET_NULL,
        verbose_name=_('Restaurant'),
        related_name='menus',
        blank=True, null=True
    )
    published = models.BooleanField(
        verbose_name=_('Published'),
        default=False, blank=False, null=False
    )


class MenuSection(TranslatableModel):
    """
    Раздел меню
    -----------

    Например, меню может иметь раздел 'супы', 'мясные блюда', 'десерты', 'напитки'...
    """
    class Meta:
        db_table = 'menus_menusection'
        # Сортировка по заголовку невозможна, если заголовок зависит от языка
        ordering = ['pk']
        verbose_name = _('menu section')
        verbose_name_plural = _('menus sections')

    translations = TranslatedFields(
        title=models.CharField(
            max_length=250,
            verbose_name=_("Title"),
            blank=False, null=False
        ),
    )
    menu = models.ForeignKey(
        to=Menu,
        on_delete=models.CASCADE,
        verbose_name=_('Menu'),
        related_name='sections',
        blank=False, null=False
    )


class MenuCourse(TranslatableModel):
    """
    Блюдо
    -----
    """
    class Meta:
        db_table = 'menus_menucourses'
        # Сортировка по заголовку невозможна, если заголовок зависит от языка
        ordering = ['pk']
        verbose_name = _('course')
        verbose_name_plural = _('courses')

    translations = TranslatedFields(
        title=models.CharField(
            max_length=250,
            verbose_name=_("Title"),
            blank=False, null=False
        ),
        composition=models.TextField(
            max_length=5000,
            verbose_name=_("Composition"),
            blank=True, null=False
        )
    )
    menu = models.ForeignKey(
        to=Menu,
        on_delete=models.CASCADE,
        verbose_name=_('Menu'),
        related_name='courses',
        blank=False, null=False
    )
    section = models.ForeignKey(
        to=MenuSection,
        on_delete=models.SET_NULL,
        verbose_name=_('Menu section'),
        related_name='courses',
        blank=True, null=True
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=False, null=False,
        verbose_name=_('Price')
    )
    published = models.BooleanField(
        verbose_name=_('Published'),
        default=False, blank=False, null=False
    )
    cooking_time = models.DurationField(
        verbose_name=_('Cooking time'),
        blank=True, null=True
    )
    options = models.JSONField(
        verbose_name=_('Options'),
        blank=True, null=True
    )
