"""
Тесты для стандартных REST API для работы с ресторанами
"""

from restaurants.tests._fixtures import BaseTestCase

from restaurants.models import Restaurant


class RestaurantRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об одиночном ресторане
    """

    def __get_url(self, restaurant_name: str = 'cheap_restaurant'):
        return f"/api/v1/restaurants/{self._data[restaurant_name].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь видит информацию о ресторане"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)

    def test_some_user(self):
        """Зарегистрированный пользователь видит информацию о ресторане"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)

    def test_cheap_owner(self):
        """Владелец ресторана видит информацию о ресторане"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)

    def test_cheap_worker(self):
        """Работник ресторана видит информацию о ресторане"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)

    def test_premium_owner(self):
        """Владелец другого ресторана видит информацию о ресторане"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)

    def test_premium_worker(self):
        """Работник другого ресторана видит информацию о ресторане"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)

    def test_admin(self):
        """Администратор видит информацию о ресторане"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)


class RestaurantListTest(BaseTestCase):
    """
    Тесты для API получения списка всех ресторанов
    """

    def __get_url(self):
        return "/api/v1/restaurants/"

    def test_unauthorized(self):
        """Неавторизованный пользователь видит список ресторанов"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_some_user(self):
        """Зарегистрированный пользователь видит список ресторанов"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_cheap_worker(self):
        """Работник дешевого ресторана видит список ресторанов"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_cheap_owner(self):
        """Владелец дешевого ресторана видит список ресторанов"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_premium_worker(self):
        """Работник дорогого ресторана видит список ресторанов"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_premium_owner(self):
        """Владелец дорогого ресторана видит список ресторанов"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_admin(self):
        """Администратор видит список ресторанов"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])


class RestaurantCreateTest(BaseTestCase):
    """
    Тесты для API создания нового ресторана
    """

    def __get_url(self):
        return "/api/v1/restaurants/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не может добавить ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        ans = self.client.post(
            self.__get_url(),
            {
                'translations': {
                    'en': {
                        'name': "New restaurant",
                        'description': "A new restaurant just added",
                    },
                    'ru': {
                        'name': "Новый ресторан",
                        'description': "Только что добавленный ресторан",
                    },
                },
                'city': 'Москва',
                'street': 'Тверская',
                'building': '25',
                'address_details': 'Вход со двора',
                'zip_code': '110120',
                'longitude': '37.5',
                'latitude': '56.5'
            },
            format='json'
        )
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был добавлен
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_some_user(self):
        """Авторизованный пользователь добавляет новый ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        with self.logged_in('some_user'):
            ans = self.client.post(
                self.__get_url(),
                {
                    'translations': {
                        'en': {
                            'name': "New restaurant",
                            'description': "A new restaurant just added",
                        },
                        'ru': {
                            'name': "Новый ресторан",
                            'description': "Только что добавленный ресторан",
                        },
                    },
                    'city': 'Москва',
                    'street': 'Тверская',
                    'building': '25',
                    'address_details': 'Вход со двора',
                    'zip_code': '110120',
                    'longitude': '37.5',
                    'latitude': '56.5'
                },
                format='json'
            )
        self.assertEqual(ans.status_code, 201)
        new_pk = ans.json()['id']
        # Проверяем, что ресторан был добавлен
        self.assertEqual(Restaurant.objects.count(), 3)
        new_restaurant = Restaurant.objects.get(pk=new_pk)
