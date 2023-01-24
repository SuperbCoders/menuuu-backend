"""
Тесты для стандартных REST API для работы с персоналом ресторанов
"""

from restaurants.tests._fixtures import BaseTestCase


class RestaurantStaffListTest(BaseTestCase):
    """
    Тесты для API получения списка всех работников ресторанов
    """

    def __get_url(self):
        return "/api/v1/restaurant_staff/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не видит список сотрудников ресторанов"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 403)

    def test_some_user(self):
        """Пользователь без работы не видит список сотрудников ресторанов"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 403)
