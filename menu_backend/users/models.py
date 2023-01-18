"""
Модели данных для пользователей системы
---------------------------------------
"""

from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Пользователь системы - владелец или сотрудник ресторана

    Содержит следующие поля.

    *   username - имя пользователя, унаследован от AbstractUser
    *   password - зашифрованный пароль, унаследован от AbstractUser
    *   email - адрес электронной почты унаследован от AbstractUser
    *   phone - номер телефона пользователя
    """
    class Meta:
        db_table = "users_user"
        ordering = ("username", )
        verbose_name = _("user")
        verbose_name_plural = _("users")

    phone = PhoneNumberField(
        verbose_name=_("phone number"),
        blank=True, null=False
    )

    def __str__(self):
        return self.username
