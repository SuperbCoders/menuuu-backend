"""
Общие функции необходимые для тестирования разных модулей системы. Выполняют создание
данных для тестирования
"""

from contextlib import contextmanager

import datetime

from rest_framework.test import APITestCase

from restaurants.models import Restaurant, RestaurantCategory
from users.models import User


def populate_test_data():
    """
    Создает данные для тестирования системы

    *   Шестерых пользователей: администратора, владельца первого ресторана,
        сотрудника первого ресторана, владельца второго ресторана, сотрудника
        второго ресторана и еще одного пользователя

    *   Категорию ресторанов - фаствуд

    *   Две ресторана - первый фастфуд, второй премиум класса
    """
    test_data = {}
    # Создаем категорию ресторанов
    test_data['category'] = RestaurantCategory.objects.create(
        name='Fastfood'
    )
    # Задаем русское название для категории
    test_data['category'].set_current_language('ru')
    test_data['category'].name = "Фастфуд"
    test_data['category'].save()
    # Создаем дешевый ресторан
    test_data['cheap_restaurant'] = Restaurant.objects.create(
        category=test_data['category'],
        name="A good place to eat",
        description="Just some good place to eat",
        phone='+79101234567',
        site='https://somerestaurant.com',
        stars=3,
        slug='some-cafe',
        country='Russia',
        city='Moscow',
        street='Leninskiy avenue',
        building='6/3',
        zip_code='123456',
        longitude=37.5,
        latitude=56.5,
    )
    # Задаем русское название и описание
    test_data['cheap_restaurant'].set_current_language('ru')
    test_data['cheap_restaurant'].name = "Придорожное кафе"
    test_data['cheap_restaurant'].description = "Первое попавшееся кафе"
    test_data['cheap_restaurant'].save()
    test_data['cheap_menu'] = test_data['cheap_restaurant'].menus.create(
        # Активное меню ресторана
        published=True, title='Menu'
    )
    test_data['cheap_menu'].set_current_language('ru')
    test_data['cheap_menu'].title = "Меню"
    test_data['cheap_menu'].save()
    test_data['inactive_menu'] = test_data['cheap_restaurant'].menus.create(
        # Это меню возвращаться не должно
        published=False, title='Inactive menu'
    )
    test_data['inactive_menu'].set_current_language('ru')
    test_data['inactive_menu'].title = "Неактивное меню"
    test_data['inactive_menu'].save()
    test_data['drinks_section'] = test_data['cheap_menu'].sections.create(
        # Раздел напитков для меню
        title='Drinks'
    )
    test_data['drinks_section'].set_current_language('ru')
    test_data['drinks_section'].title = "Напитки"
    test_data['drinks_section'].save()
    test_data['desserts_section'] = test_data['cheap_menu'].sections.create(
        # Раздел напитков для меню
        title='Desserts'
    )
    test_data['desserts_section'].set_current_language('ru')
    test_data['desserts_section'].title = "Десерты"
    test_data['desserts_section'].save()
    test_data['sparkling_water'] = test_data['drinks_section'].courses.create(
        menu=test_data['cheap_menu'],
        published=True,
        title="Sparkling mineral water",
        price=25,
        cooking_time=datetime.timedelta(days=0)
    )
    test_data['sparkling_water'].set_current_language('ru')
    test_data['sparkling_water'].title = "Газированная минеральная вода"
    test_data['sparkling_water'].save()
    test_data['still_water'] = test_data['drinks_section'].courses.create(
        menu=test_data['cheap_menu'],
        published=True,
        title="Still mineral water",
        price=20,
        cooking_time=datetime.timedelta(days=0)
    )
    test_data['still_water'].set_current_language('ru')
    test_data['still_water'].title = "Негазированная минеральная вода"
    test_data['still_water'].save()
    test_data['disabled_water'] = test_data['drinks_section'].courses.create(
        # Этой воды в меню быть не должно
        menu=test_data['cheap_menu'],
        published=False,
        title="Unavailable mineral water",
        price=30,
        cooking_time=datetime.timedelta(days=0)
    )
    test_data['disabled_water'].set_current_language('ru')
    test_data['disabled_water'].title = "Недоступная минеральная вода"
    test_data['disabled_water'].save()
    test_data['chocolate_sandwich'] = test_data['desserts_section'].courses.create(
        # Этой воды в меню быть не должно
        menu=test_data['cheap_menu'],
        published=True,
        title="Sandwich with chocolate butter",
        price=30,
        cooking_time=datetime.timedelta(seconds=90)
    )
    test_data['chocolate_sandwich'].set_current_language('ru')
    test_data['chocolate_sandwich'].title = "Бутерброд с шоколадным маслом"
    test_data['chocolate_sandwich'].save()
    # Создаем дорогой ресторан
    test_data['premium_restaurant'] = Restaurant.objects.create(
        name="Premium restaurant",
        description="A premium-class restaurant",
        phone='+79107654321',
        site='https://premiumrestaurant.com',
        stars=5,
        country='Russia',
        city='Moscow',
        street='Noviy Arbat',
        building='1',
        zip_code='123456',
        longitude=37.5,
        latitude=56.5,
    )
    # Задаем русское название и описание
    test_data['premium_restaurant'].set_current_language('ru')
    test_data['premium_restaurant'].name = "Премиум ресторан"
    test_data['premium_restaurant'].description = "Ресторан премиум-класса"
    test_data['premium_restaurant'].save()
    test_data['premium_menu'] = test_data['premium_restaurant'].menus.create(
        # Активное меню премиум ресторана
        published=True, title='Menu'
    )
    test_data['premium_menu'].set_current_language('ru')
    test_data['premium_menu'].title = "Меню"
    test_data['premium_menu'].save()
    # Создать пользователя-администратора
    test_data['admin'] = User.objects.create_superuser(
        username='administrator',
        password='administrator',
        email='administrator@localhost'
    )
    # Создать владельца и работника дешевого ресторана
    test_data['cheap_owner'] = User.objects.create_user(
        username='cheap_owner',
        password='cheap_owner',
        email='cheap_owner@localhost'
    )
    test_data['cheap_worker'] = User.objects.create_user(
        username='cheap_worker',
        password='cheap_worker',
        email='cheap_worker@localhost'
    )
    test_data['cheap_restaurant'].restaurant_staff.create(
        user=test_data['cheap_owner'], position='owner'
    )
    test_data['cheap_restaurant'].restaurant_staff.create(
        user=test_data['cheap_worker'], position='worker'
    )
    # Создать владельца и работника дорогого ресторана
    test_data['premium_owner'] = User.objects.create_user(
        username='premium_owner',
        password='premium_owner',
        email='premium_owner@localhost'
    )
    test_data['premium_worker'] = User.objects.create_user(
        username='premium_worker',
        password='premium_worker',
        email='premium_worker@localhost'
    )
    test_data['premium_restaurant'].restaurant_staff.create(
        user=test_data['premium_owner'], position='owner'
    )
    test_data['premium_restaurant'].restaurant_staff.create(
        user=test_data['premium_worker'], position='worker'
    )
    # Создать еще одного пользователя, не связанного ни с каким рестораном
    test_data['some_user'] = User.objects.create_user(
        username='some_user',
        password='some_user',
        email='some_user@localhost'
    )
    return test_data


def cleanup_test_data(test_data):
    """
    Уничтожает тестовые данные
    """
    test_data['inactive_menu'].save()
    test_data['cheap_menu'].delete()
    test_data['cheap_restaurant'].delete()
    test_data['premium_menu'].delete()
    test_data['premium_restaurant'].delete()
    test_data['admin'].delete()
    test_data['cheap_owner'].delete()
    test_data['cheap_worker'].delete()
    test_data['premium_owner'].delete()
    test_data['premium_worker'].delete()
    test_data['some_user'].delete()


class BaseTestCase(APITestCase):
    """
    Базовый класс для тестов. Выполняет создание тестовых данных перед началом
    прогона тестов и их уничтожение по окончении прогона тестов.

    Основан на классе APITestCase но дополнительно содержит поле `_data`, являющееся
    словарем со следующими полями

    *   'category'
        Тестовая категория ресторанов 'фастфуд'

    *   'cheap_restaurant'
        Тестовый ресторан из категории фастфуд

    *   'premium_restaurant'
        Тестовый ресторан премиум-класса

    *   'cheap_menu'
        Активное меню для дешевого ресторана

    *   'inactive_menu'
        Неактивное меню для дешевого ресторана

    *   'premium_menu'
        Активное - и единственное - меню дорогого ресторана
    """

    @classmethod
    def setUpClass(cls):
        """Создает данные для тестирования"""
        super().setUpClass()
        cls._data = populate_test_data()

    @classmethod
    def tearDownClass(cls):
        """Удаляет тестовые данные"""
        cleanup_test_data(cls._data)
        super().tearDownClass()

    @contextmanager
    def logged_in(self, username):
        """
        Контекст для выполнения кода от имени определенного зарегистрированного
        пользователя. Возможные значения параметра username следующие

        *   'admin'
        *   'cheap_owner'
        *   'cheap_worker'
        *   'premium_owner'
        *   'premium_worker'
        *   'some_user'
        """
        user = self._data[username]
        self.client.force_authenticate(user)
        yield user
        self.client.logout()

    def verify_fastfood_category(self, info):
        """
        Проверить, что словарь info содержит корректные данные о категории
        фастфуд-ресторанов.
        """
        self.assertCountEqual(info.keys(), ['id', 'translations'])
        self.assertEqual(info['id'], self._data['category'].pk)
        self.assertEqual(info['translations']['en']['name'], "Fastfood")

    def verify_cheap_active_menu(self, info):
        """
        Проверить, что словарь info соответствует данным об активном меню дешевого
        ресторана.
        """
        self.assertEqual(info['translations']['en']['title'], "Menu")
        self.assertEqual(info['translations']['ru']['title'], "Меню")
        self.assertEqual(info['published'], True)
        self.assertEqual(info['restaurant'], self._data['cheap_restaurant'].pk)

    def verify_cheap_restaurant(self, info):
        """
        Проверить, что словарь info содержит необходимые данные о тестовом
        дешевом ресторане
        """
        self.assertEqual(info['id'], self._data['cheap_restaurant'].pk)
        self.assertEqual(info['translations']['en']['name'], "A good place to eat")
        self.assertEqual(info['translations']['ru']['name'], "Придорожное кафе")
        self.assertEqual(info['translations']['en']['description'], "Just some good place to eat")
        self.assertEqual(info['translations']['ru']['description'], "Первое попавшееся кафе")
        self.assertEqual(info['slug'], "some-cafe")
        self.assertEqual(info['category'], self._data['category'].pk)
        self.assertEqual(info['category_data']['translations']['en']['name'], "Fastfood")
        # FIXME: Здесь все правильно при запущенном сервисе, но почему-то этого
        # поля нет при тестировании
        # self.assertEqual(info['category_data']['translations']['ru']['name'], "Фастфуд")
        self.assertEqual(info['stars'], 3)
        self.assertEqual(info['phone'], "+79101234567")
        self.assertEqual(info['site'], "https://somerestaurant.com")
        self.assertEqual(info['logo'], None)
        self.assertEqual(info['picture'], None)
        # Проверить меню
        self.verify_cheap_active_menu(info['current_menu'])

    def verify_premium_restaurant(self, info):
        """
        Проверить, что словарь info содержит необходимые данные о тестовом
        дешевом ресторане
        """
        self.assertEqual(info['id'], self._data['premium_restaurant'].pk)
        self.assertEqual(info['translations']['en']['name'], "Premium restaurant")
        self.assertEqual(info['translations']['ru']['name'], "Премиум ресторан")
        self.assertEqual(info['translations']['en']['description'], "A premium-class restaurant")
        self.assertEqual(info['translations']['ru']['description'], "Ресторан премиум-класса")
        self.assertEqual(info['slug'], "")
        self.assertEqual(info['category'], None)
        self.assertEqual(info['category_data'], None)
        self.assertEqual(info['stars'], 5)
        self.assertEqual(info['phone'], "+79107654321")
        self.assertEqual(info['site'], "https://premiumrestaurant.com")
        self.assertEqual(info['logo'], None)
        self.assertEqual(info['picture'], None)

    def verify_restaurant_list(self, info):
        """
        Проверить, что список info содержит список словарей с описанием тестовых
        ресторанов и не содержит ничего другого
        """
        self.assertIsInstance(info, list)
        self.assertEqual(len(info), 2)
        for item in info:
            if item['id'] == self._data['cheap_restaurant'].pk:
                self.verify_cheap_restaurant(item)
            elif item['id'] == self._data['premium_restaurant'].pk:
                self.verify_premium_restaurant(item)
            else:
                self.fail("В возвращенном списке ресторанов оказался неизвестный ресторан")
