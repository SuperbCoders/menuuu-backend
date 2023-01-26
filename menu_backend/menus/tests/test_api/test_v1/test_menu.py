"""
Тесты для API для работы с меню
"""

from restaurants.tests._fixtures import BaseTestCase


class MenuListTest(BaseTestCase):
    """
    Тесты для API получения списка меню
    """

    URL = '/api/v1/menu/'

    def test_unauthorized(self):
        """Неавторизованный пользователь видит все опубликованные меню"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.assertEqual(len(info['results']), 2)

    def test_some_user(self):
        """Зарегистрированный пользователь видит все опубликованные меню"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.assertEqual(len(info['results']), 2)

    def test_cheap_worker(self):
        """Работник ресторана видит неопубликованные меню своего ресторана"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_cheap_owner(self):
        """Хозяин ресторана видит неопубликованные меню своего ресторана"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_premium_worker(self):
        """Работник не видит неопубликованные меню чужого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.assertEqual(len(info['results']), 2)

    def test_premium_owner(self):
        """Владелец не видит неопубликованные меню чужого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.assertEqual(len(info['results']), 2)

    def test_admin(self):
        """Администратор видит все опубликованные меню включая неопубликованные"""
        with self.logged_in('admin'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)


class MenuRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об определенном меню
    """

    def __get_url(self):
        return f"/api/v1/menu/{self._data['cheap_menu'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь может видеть опубликованное меню"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)