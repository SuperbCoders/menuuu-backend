"""
Тесты для API для работы с разделами меню
"""

from restaurants.tests._fixtures import BaseTestCase


class MenuSectionListTest(BaseTestCase):
    """
    Тесты для API получения списка разделов меню
    """

    URL = '/api/v1/menu_sections/'

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает список всех разделов меню"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
