"""
Тесты для получения пользователем списка проблем со своими ресторанами
"""

from restaurants.tests._fixtures import BaseTestCase


class MyProblemsTestCase(BaseTestCase):
    """
    Тесты для доступа к функции получения списка проблем со своими ресторанами
    """

    def __get_url(self):
        return '/api/v1/users/my_problems/'

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
        """Владелец ресторана видит список проблем этого ресторана"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        print(info)
        self.assertCountEqual(info.keys(), ['count', 'results'])
        self.assertEqual(info['count'], 0)
        self.assertEqual(info['results'], [])
