"""
Модели данных для ресторанов и персонала ресторанов
---------------------------------------------------

Содержит следующие модели данных.

*   Категория ресторанов
*   Ресторан
*   Сотрудник или владелец ресторана
"""

import qrcode
import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields

from phonenumber_field.modelfields import PhoneNumberField

from users.models import User


class RestaurantCategory(TranslatableModel):
    """
    Категория ресторанов
    --------------------
    """
    class Meta:
        db_table = 'restaurants_restaurantcategory'
        ordering = ['pk']
        verbose_name = _('restaurant category')
        verbose_name_plural = _('restaurant categories')

    translations = TranslatedFields(
        name=models.CharField(
            max_length=100,
            verbose_name=_("Category name"),
            blank=False, null=False
        )
    )

    def __str__(self):
        return self.name


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
    slug = models.SlugField(
        verbose_name=_("Nickname"),
        max_length=100,
        unique=True,
        blank=False,
        null=False
    )
    logo = models.ImageField(
        verbose_name=_("Logo"),
        blank=True, null=True
    )
    picture = models.ImageField(
        verbose_name=_("Picture"),
        blank=True, null=True
    )
    category = models.ForeignKey(
        to=RestaurantCategory,
        verbose_name=_("Restaurant category"),
        on_delete=models.SET_NULL,
        related_name='restaurants',
        blank=True, null=True
    )
    stars = models.PositiveSmallIntegerField(
        verbose_name=_("Number of stars"),
        default=0,
        blank=False, null=False
    )
    country = models.CharField(
        max_length=100,
        verbose_name=_("Country"),
        blank=False,
        null=False
    )
    city = models.CharField(
        max_length=100,
        verbose_name=_("City"),
        blank=False,
        null=False
    )
    street = models.CharField(
        max_length=100,
        verbose_name=_("Street"),
        blank=True,
        null=False
    )
    building = models.CharField(
        max_length=20,
        verbose_name=_("Building"),
        blank=False,
        null=False
    )
    address_details = models.CharField(
        max_length=100,
        verbose_name=_("Address details"),
        blank=True,
        null=False
    )
    zip_code = models.CharField(
        max_length=20,
        verbose_name=_("Zip code"),
        blank=False,
        null=False
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
    phone = PhoneNumberField(
        verbose_name=_("Phone number"),
        blank=True, null=False
    )
    site = models.URLField(
        max_length=100,
        verbose_name=_("Site URL"),
        blank=True, null=False
    )
    twitter_profile = models.URLField(
        max_length=100,
        verbose_name=_("Twitter profile URL"),
        blank=True, null=True
    )
    facebook_profile = models.URLField(
        max_length=100,
        verbose_name=_("Facebook profile URL"),
        blank=True, null=True
    )
    instagram_profile = models.URLField(
        max_length=100,
        verbose_name=_("Instagram profile URL"),
        blank=True, null=True
    )
    average_receipt = models.DecimalField(
        max_digits=10, decimal_places=2,
        blank=True, null=True,
        verbose_name=_('Average receipt price')
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Сохранить данные о ресторане. Если для ресторана не задано сокращенное название
        для URL то сгенерировать его автоматически на основе его первичного ключа
        """
        if self.pk:
            if self.slug:
                self.slug = self.slug.lower()
            else:
                self.slug = f"id_{self.pk}"
            super().save(*args, **kwargs)
        elif not self.slug:
            self.slug = "id__"
            super().save(*args, **kwargs)
            self.slug = f"id_{self.pk}"
            super().save()
        else:
            super().save(*args, **kwargs)

    @property
    def current_menu(self):
        """Возвращает текущее активное меню ресторана"""
        return self.menus.filter(published=True).first()

    def generate_qrcode(self):
        """Генерирует QR код для доступа к меню ресторана через API"""
        logger = logging.getLogger('root')
        data = settings.SITE_URL + "/" + self.slug + "/"
        logger.info(_("Generating a QR code for URL: {}").format(data))
        img = qrcode.make(data)
        return img

    def check_owner(self, user):
        """
        Возвращает True, если пользователь user является владельцем ресторана
        self и False в противном случае
        """
        if not user.is_authenticated or not user.is_active:
            return False
        return self.restaurant_staff.filter(position='owner', user=user).exists()

    def check_owner_or_worker(self, user):
        """
        Возвращает True, если пользователь user является владельцем ресторана
        self или работает в нем и False в противном случае
        """
        if not user.is_authenticated or not user.is_active:
            return False
        return self.restaurant_staff.filter(user=user).exists()

    def get_problems(self):
        """
        Возвращает список текстовых строк с описанием проблем с данными о ресторане,
        включая отсутствие владельца, отсутствие опубликованного меню, пустые разделы
        меню и т.п.
        """
        problems = []
        if not self.restaurant_staff.filter(position='owner').exists():
            problems.append(f"Ресторан {self.name} не имеет пользователя-владельца")
        if self.current_menu is None:
            problems.append(f"Ресторан {self.name} не имеет опубликованного меню")
        if not self.current_menu.all_published_courses.exists():
            problems.append(f"Меню ресторана {self.name} пусто")
        for section in self.current_menu.sections.filter(published=True).all():
            if not section.courses.filter(published=True).exists():
                problems.append(f"Раздел {section.name} меню ресторана {self.name} пуст")
        return problems


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
        verbose_name_plural = _('restaurant ownerships or employments')

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
