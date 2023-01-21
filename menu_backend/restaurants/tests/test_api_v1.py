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
        self.verify_cheap_restaurant(info)

    def test_admin(self):
        """Администратор видит информацию о ресторане"""
        with self.logged_in('admin'):
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


class RestaurantListTest(BaseTestCase):
    """
    Тесты для API получения списка всех ресторанов
    """

    def __get_url(self):
        return f"/api/v1/restaurants/"

    def test_unauthorized(self):
        """Неавторизованный пользователь видит список ресторанов"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        results = info['results']
        self.assertEqual(len(results), 2)
        for res in results:
            if res['id'] == self._data['cheap_restaurant'].pk:
                self.verify_cheap_restaurant(res)
            elif res['id'] == self._data['premium_restaurant'].pk:
                pass
            else:
                self.fail("В возвращенном списке ресторанов оказался неизвестный ресторан")
