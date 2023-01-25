"""
Тесты для API для работы с блюдами
"""

from restaurants.tests._fixtures import BaseTestCase


class MenuCourseListTest(BaseTestCase):
    """
    Тесты для API получения списка блюд
    """

    def __get_url(self):
        return '/api/v1/menu_courses/'

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает список всех опубликованных блюд"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_some_user(self):
        """Пользователь без разрешений просматривает список всех опубликованных блюд"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_cheap_worker(self):
        """Сотрудник первого ресторана видит все бдюда включая неопубликованные"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 4)
        self.assertEqual(len(info['results']), 4)

    def test_cheap_owner(self):
        """Хозяин первого ресторана видит все бдюда включая неопубликованные"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 4)
        self.assertEqual(len(info['results']), 4)

    def test_premium_worker(self):
        """Работник ресторана не видит неопубликованных блюд другого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_premium_owner(self):
        """Хозяин ресторана не видит неопубликованных блюд другого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_admin(self):
        """Администратор видит все бдюда включая неопубликованные"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 4)
        self.assertEqual(len(info['results']), 4)


class PublishedMenuCourseRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об определенном опубликованном блюде
    """

    def __get_url(self):
        return f"/api/v1/menu_courses/{self._data['chocolate_sandwich'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь может видеть опубликованное блюдо"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())

    def test_some_user(self):
        """Зарегистрированный пользователь может видеть опубликованное блюдо"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())
