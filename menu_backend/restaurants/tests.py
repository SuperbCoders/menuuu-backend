"""
Тесты для API работы с ресторанами
"""

import datetime

from rest_framework.test import APITestCase

from restaurants.models import Restaurant, RestaurantCategory


class PublicRestaurantTestCase(APITestCase):
    """
    Тесты для API общедоступного меню ресторана
    """

    def setUp(self):
        """Создать данные для тестирования"""
        # Создаем категорию ресторанов
        self.category = RestaurantCategory.objects.create(
            name='Fastfood'
        )
        # Задаем русское название для категории
        self.category.set_current_language('ru')
        self.category.name = "Фастфуд"
        self.category.save()
        # Создаем ресторан
        self.restaurant = Restaurant.objects.create(
            category=self.category,
            name="A good place to eat",
            description="Just some good place to eat",
            phone='+79101234567',
            site='https://somerestaurant.com',
            stars=3,
            country='Russia',
            city='Moscow',
            street='Leninskiy avenue',
            building='6/3',
            zip_code='123456',
            longitude=37.5,
            latitude=56.5,
        )
        # Задаем русское название и описание
        self.restaurant.set_current_language('ru')
        self.restaurant.name = "Придорожное кафе"
        self.restaurant.description = "Первое попавшееся кафе"
        self.restaurant.save()
        self.menu = self.restaurant.menus.create(
            # Активное меню ресторана
            published=True, title='Menu'
        )
        self.menu.set_current_language('ru')
        self.menu.title = "Меню"
        self.menu.save()
        self.inactive_menu = self.restaurant.menus.create(
            # Это меню возвращаться не должно
            published=True, title='Inactive menu'
        )
        self.inactive_menu.set_current_language('ru')
        self.inactive_menu.title = "Неактивное меню"
        self.inactive_menu.save()
        self.drinks_section = self.menu.sections.create(
            # Раздел напитков для меню
            title='Drinks'
        )
        self.drinks_section.set_current_language('ru')
        self.drinks_section.title = "Напитки"
        self.drinks_section.save()
        self.desserts_section = self.menu.sections.create(
            # Раздел напитков для меню
            title='Desserts'
        )
        self.desserts_section.set_current_language('ru')
        self.desserts_section.title = "Десерты"
        self.desserts_section.save()
        self.sparkling_water = self.drinks_section.courses.create(
            menu=self.menu,
            published=True,
            title="Sparkling mineral water",
            price=25,
            cooking_time=datetime.timedelta(days=0)
        )
        self.sparkling_water.set_current_language('ru')
        self.sparkling_water.title = "Газированная минеральная вода"
        self.sparkling_water.save()
        self.still_water = self.drinks_section.courses.create(
            menu=self.menu,
            published=True,
            title="Still mineral water",
            price=20,
            cooking_time=datetime.timedelta(days=0)
        )
        self.still_water.set_current_language('ru')
        self.still_water.title = "Негазированная минеральная вода"
        self.still_water.save()
        self.disabled_water = self.drinks_section.courses.create(
            # Этой воды в меню быть не должно
            menu=self.menu,
            published=False,
            title="Unavailable mineral water",
            price=30,
            cooking_time=datetime.timedelta(days=0)
        )
        self.disabled_water.set_current_language('ru')
        self.disabled_water.title = "Недоступная минеральная вода"
        self.disabled_water.save()
        self.chocolate_sandwich = self.desserts_section.courses.create(
            # Этой воды в меню быть не должно
            menu=self.menu,
            published=True,
            title="Sandwich with chocolate butter",
            price=30,
            cooking_time=datetime.timedelta(seconds=90)
        )
        self.chocolate_sandwich.set_current_language('ru')
        self.chocolate_sandwich.title = "Бутерброд с шоколадным маслом"
        self.chocolate_sandwich.save()

    def tearDown(self):
        """Удалить тестовые данные"""
        self.inactive_menu.save()
        self.menu.delete()
        self.restaurant.delete()

    def __get_url(self):
        """URL для запроса информации о ресторане"""
        return f"/api/v1/public/restaurants/{self.restaurant.pk}/"

    def __get_section_from_answer(self, info, section_name):
        """Ищет в информации о ресторане данные о разделе меню"""
        for section in info['menu']['sections']:
            if section['title'] == section_name:
                return section
        self.assertFalse(f"Раздел меню '{section_name}' не найден")

    def test_restaurant_name(self):
        """Возвращается название и описание ресторана"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['name'], "A good place to eat")
        self.assertEqual(info['description'], "Just some good place to eat")
        self.assertEqual(info['stars'], 3)
        from pprint import PrettyPrinter
        PrettyPrinter().pprint(info)

    def test_restaurant_name_ru(self):
        """Возвращается название и описание ресторана по-русски"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['name'], "Придорожное кафе")
        self.assertEqual(info['description'], "Первое попавшееся кафе")
        self.assertEqual(info['stars'], 3)
        from pprint import PrettyPrinter
        PrettyPrinter().pprint(info)

    def test_restaurant_category(self):
        """Возвращается название категории ресторана"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['category']['name'], "Fastfood")

    def test_restaurant_category_ru(self):
        """Возвращается название категории ресторана по русски"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['category']['name'], "Фастфуд")

    def test_restaurant_address(self):
        """Возвращается адрес и координаты ресторана"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()['address']
        self.assertEqual(info['country'], "Russia")
        self.assertEqual(info['city'], "Moscow")
        self.assertEqual(info['street'], "Leninskiy avenue")
        self.assertEqual(info['building'], "6/3")
        self.assertEqual(info['address_details'], "")
        self.assertEqual(info['zip_code'], "123456")
        self.assertEqual(info['latitude'], 56.5)
        self.assertEqual(info['longitude'], 37.5)

    def test_restaurant_address_ru(self):
        """Адрес и координаты ресторана не зависят от языка"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = ans.json()['address']
        self.assertEqual(info['country'], "Russia")
        self.assertEqual(info['city'], "Moscow")
        self.assertEqual(info['street'], "Leninskiy avenue")
        self.assertEqual(info['building'], "6/3")
        self.assertEqual(info['address_details'], "")
        self.assertEqual(info['zip_code'], "123456")
        self.assertEqual(info['latitude'], 56.5)
        self.assertEqual(info['longitude'], 37.5)

    def test_restaurant_contacts(self):
        """Возвращается номер телефона и сайт ресторана"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['phone'], "+79101234567")
        self.assertEqual(info['site'], "https://somerestaurant.com")

    def test_restaurant_contacts_ru(self):
        """Номер телефона и адрес сайта возвращаются для русского языка"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['phone'], "+79101234567")
        self.assertEqual(info['site'], "https://somerestaurant.com")

    def test_menu_title(self):
        """Заголовок меню возвращается корректно"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()['menu']
        self.assertEqual(info['title'], "Menu")
        self.assertEqual(info['courses'], [])

    def test_menu_title_ru(self):
        """Заголовок меню возвращается корректно по русски"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = ans.json()['menu']
        self.assertEqual(info['title'], "Меню")
        self.assertEqual(info['courses'], [])

    def test_menu_section_titles(self):
        """Заголовки разделов меню возвращаются корректно"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()['menu']['sections']
        self.assertCountEqual(
            [item['title'] for item in info],
            ['Desserts', 'Drinks']
        )

    def test_menu_section_titles_ru(self):
        """Заголовки разделов меню возвращаются корректно по русски"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = ans.json()['menu']['sections']
        self.assertCountEqual(
            [item['title'] for item in info],
            ['Десерты', 'Напитки']
        )

    def test_drink_titles(self):
        """Заголовки напитков возвращаются корректно"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = self.__get_section_from_answer(ans.json(), 'Drinks')
        self.assertCountEqual(
            [item['title'] for item in info['courses']],
            ['Sparkling mineral water', 'Still mineral water']
        )

    def test_drink_titles_ru(self):
        """Заголовки напитков возвращаются корректно на русском языке"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = self.__get_section_from_answer(ans.json(), 'Напитки')
        self.assertCountEqual(
            [item['title'] for item in info['courses']],
            ['Газированная минеральная вода', 'Негазированная минеральная вода']
        )

    def test_drink_prices(self):
        """Цены напитков возвращаются корректно"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = self.__get_section_from_answer(ans.json(), 'Drinks')
        self.assertCountEqual(
            [item['price'] for item in info['courses']],
            [20, 25]
        )

    def test_drink_prices_ru(self):
        """Цены напитков возвращаются корректно при разных настройках языке"""
        ans = self.client.get(self.__get_url(), {'language': 'ru'})
        self.assertEqual(ans.status_code, 200)
        info = self.__get_section_from_answer(ans.json(), 'Напитки')
        self.assertCountEqual(
            [item['price'] for item in info['courses']],
            [20, 25]
        )
