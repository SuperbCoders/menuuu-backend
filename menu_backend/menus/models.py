"""
Модели данных для меню и блюд
-----------------------------

Включает следующие модели данных

*   Меню
*   Раздел меню
*   Блюдо
"""

from django.db import models
from django.db.models import Q
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
        verbose_name = _('menu')
        verbose_name_plural = _('menus')

    translations = TranslatedFields(
        title=models.CharField(
            max_length=250,
            verbose_name=_("Title"),
            blank=False, null=False
        ),
    )
    restaurant = models.ForeignKey(
        to=Restaurant,
        on_delete=models.CASCADE,
        verbose_name=_('Restaurant'),
        related_name='menus',
        blank=False, null=False
    )
    published = models.BooleanField(
        verbose_name=_('Published'),
        default=False, blank=False, null=False
    )

    def __str__(self):
        if self.restaurant:
            return f"{self.title} at {self.restaurant.name}"
        return self.title

    @property
    def extra_published_courses(self):
        """Список опубликованных блюд меню, не входящих ни в один подраздел"""
        return self.courses.filter(section__isnull=True, published=True)

    def check_published(self):
        """
        Проверить, что меню опубликовано
        """
        return self.published

    def check_restaurant_staff(self, user):
        """
        Проверить, что пользователь работает в ресторане, к которому относится меню
        """
        return self.restaurant.check_owner_or_worker(user)

    @property
    def all_published_courses(self):
        """
        Возвращает Queryset со списком всех опубликованных блюд в опубликованных
        разделах меню.
        """
        return self.courses.filter(
            Q(published=True) & (
                Q(section__isnull=True) | Q(section__published=True)
            )
        )

    def save(self, *args, **kwargs):
        """
        Если меню сделано опубликованным, то автоматически все другие меню того же
        ресторана должны стать неопубликованными
        """
        super().save(*args, **kwargs)
        if self.restaurant and self.published:
            for other_menu in self.restaurant.menus.exclude(pk=self.pk).all():
                other_menu.published = False
                other_menu.save()


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
    published = models.BooleanField(
        verbose_name=_('Published'),
        default=True, blank=False, null=False
    )

    def __str__(self):
        return self.title

    @property
    def published_courses(self):
        """Список опубликованных блюд, входящих в подраздел"""
        return self.courses.filter(published=True)

    def check_published(self):
        """
        Проверить, что меню, к которому относится этот раздел, опубликовано
        """
        return self.published and self.menu.check_published()

    def check_restaurant_staff(self, user):
        """
        Проверить, что пользователь работает в ресторане, к которому относится меню
        """
        return self.menu.check_restaurant_staff(user)


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
        default=True, blank=False, null=False
    )
    cooking_time = models.DurationField(
        verbose_name=_('Cooking time'),
        blank=True, null=True
    )
    options = models.JSONField(
        verbose_name=_('Options'),
        blank=True, null=True
    )

    def __str__(self):
        return self.title

    def check_published(self):
        """
        Проверить, что меню, к которому относится это блюдо, опубликовано и
        само блюдо также опубликовано.
        """
        return self.published and self.section.check_published()

    def check_restaurant_staff(self, user):
        """
        Проверить, что пользователь работает в ресторане, к которому относится меню
        """
        return self.menu.check_restaurant_staff(user)
