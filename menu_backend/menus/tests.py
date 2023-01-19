"""
Тесты для API для работы с меню, разделами меню и блюдами
"""

from rest_framework.test import APITestCase

from menus.models import Menu, MenuSection, MenuCourse


class MenuTestCase(APITestCase):
    """
    Базовый класс для тестов приложения для работы с меню. Он создает в базе
    данных системы меню для тестирования и удаляет его после прогона тестов.
    """

    def setUp(self):
        """Создает данные для тестирования"""
        self._menu_first = Menu.objects.create(title='First menu', published=True)
        self._menu_second = Menu.objects.create(title='Second menu', published=True)
        self._menu_disabled = Menu.objects.create(title='Disabled menu', published=False)
        self._section_1a = MenuSection.objects.create(menu=self._menu_first, title="Snacks")
        self._section_1b = MenuSection.objects.create(menu=self._menu_first, title="Main courses")
        self._section_1d = MenuSection.objects.create(menu=self._menu_first, title="Desserts")
        self._section_1c = MenuSection.objects.create(menu=self._menu_first, title="Drinks")
        self._course_1a = MenuCourse.objects.create(
            menu=self._menu_first,
            section=self._section_1a,
            title="First snack",
            price=100,
            published=True
        )

    def tearDown(self):
        """Удаляет тестовые данные"""
        self._menu_first.delete()
        self._menu_second.delete()
        self._menu_disabled.delete()


class MenuCourseListTest(MenuTestCase):
    """
    Тесты для API получения списка блюд
    """

    URL = '/api/v1/menu_courses/'

    def test_unauthorized(self):
        """Неавторизованный пользователь не имеет доступа к странице списка всех блюд"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 403)


class MenuSectionListTest(MenuTestCase):
    """
    Тесты для API получения списка разделов меню
    """

    URL = '/api/v1/menu_sections/'

    def test_unauthorized(self):
        """Неавторизованный пользователь не имеет доступа к странице списка всех разделов меню"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 403)


class MenuListTest(MenuTestCase):
    """
    Тесты для API получения списка меню
    """

    URL = '/api/v1/menu/'

    def test_unauthorized(self):
        """Неавторизованный пользователь не имеет доступа к странице списка всех меню"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 403)
