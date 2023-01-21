"""
Тесты для API для работы с меню, разделами меню и блюдами
"""

from menus.models import Menu, MenuSection, MenuCourse

from restaurants.tests._fixtures import BaseTestCase


class MenuCourseListTest(BaseTestCase):
    """
    Тесты для API получения списка блюд
    """

    URL = '/api/v1/menu_courses/'

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает список всех блюд"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)


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
        """Неавторизованный пользователь просматривает список всех меню"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)
