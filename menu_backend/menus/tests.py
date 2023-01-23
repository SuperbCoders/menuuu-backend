"""
Тесты для API для работы с меню, разделами меню и блюдами
"""

from restaurants.tests._fixtures import BaseTestCase


class MenuCourseListTest(BaseTestCase):
    """
    Тесты для API получения списка блюд
    """

    def __get_url(self):
        return '/api/v1/menu_courses/'

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает список всех блюд"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)


class MenuCourseRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об определенном блюде
    """

    def __get_url(self):
        return f"/api/v1/menu_courses/{self._data['chocolate_sandwich'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь может видеть опубликованное блюдо"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()


class MenuSectionListTest(BaseTestCase):
    """
    Тесты для API получения списка разделов меню
    """

    URL = '/api/v1/menu_sections/'

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает список всех разделов меню"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)


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
