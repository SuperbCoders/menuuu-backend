"""
Тесты для получения пользователем списка своих ресторанов
"""

from restaurants.tests._fixtures import BaseTestCase


class MyRestaurantsTestCase(BaseTestCase):
    """
    Тесты для доступа к функции получения списка своих ресторанов
    """

    def __get_url(self):
        return '/api/v1/users/my_restaurants/'

    def test_unauthorized(self):
        """Неавторизованный пользователь получает ошибку"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 401)

    def test_some_user(self):
        """Зарегистрированный пользователь не владеющий рестораном видит пустой список"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['count', 'results'])
        self.assertEqual(info['count'], 0)
        self.assertEqual(info['results'], [])

    def test_cheap_owner(self):
        """Владелец фастфуд-ресторана видит информацию о своем ресторане"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['count', 'results'])
        self.assertEqual(info['count'], 1)
        self.verify_cheap_restaurant(info['results'][0])

    def test_cheap_worker(self):
        """Сотрудник ресторана, не владеющий рестораном, видит пустой список"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['count', 'results'])
        self.assertEqual(info['count'], 0)
        self.assertEqual(info['results'], [])

    def test_premium_owner(self):
        """Владелец премиум-ресторана видит информацию о своем ресторане"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['count', 'results'])
        self.assertEqual(info['count'], 1)
        self.verify_premium_restaurant(info['results'][0])

    def test_premium_worker(self):
        """Сотрудник ресторана, не владеющий рестораном, видит пустой список"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['count', 'results'])
        self.assertEqual(info['count'], 0)
        self.assertEqual(info['results'], [])

    def test_admin(self):
        """Админисратор не владеющий рестораном видит пустой список"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['count', 'results'])
        self.assertEqual(info['count'], 0)
        self.assertEqual(info['results'], [])
