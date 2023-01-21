"""
Тесты для API работы с ресторанами
"""

from restaurants.tests._fixtures import BaseTestCase


class PublicRestaurantTestCase(BaseTestCase):
    """
    Тесты для API общедоступного меню ресторана
    """

    def __get_url(self):
        """URL для запроса информации о ресторане"""
        return f"/api/v1/public/restaurants/{self._data['cheap_restaurant'].pk}/"

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
