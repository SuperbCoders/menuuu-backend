"""
Тесты для стандартных REST API для работы с ресторанами
"""

from restaurants.tests._fixtures import BaseTestCase


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
        from pprint import PrettyPrinter
        PrettyPrinter().pprint(info)
