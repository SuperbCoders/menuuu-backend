"""
Тесты для API для работы с меню
"""

from restaurants.tests._fixtures import BaseTestCase

from menus.models import Menu


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


class PublishedMenuRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об определенном опубликованном меню
    """

    def __get_url(self):
        return f"/api/v1/menu/{self._data['cheap_menu'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает опубликованное меню"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_active_menu(ans.json())

    def test_some_user(self):
        """Авторизованный пользователь просматривает опубликованное меню"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_active_menu(ans.json())

    def test_cheap_worker(self):
        """Работник дешевого ресторана просматривает опубликованное меню"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_active_menu(ans.json())

    def test_cheap_owner(self):
        """Хозяин дешевого ресторана просматривает опубликованное меню"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_active_menu(ans.json())

    def test_premium_worker(self):
        """Работник дешевого ресторана просматривает опубликованное меню"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_active_menu(ans.json())

    def test_premium_owner(self):
        """Хозяин дешевого ресторана просматривает опубликованное меню"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_active_menu(ans.json())

    def test_admin(self):
        """Администратор просматривает опубликованное меню"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_active_menu(ans.json())


class UnpublishedMenuRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об определенном неопубликованном меню
    """

    def __get_url(self):
        return f"/api/v1/menu/{self._data['inactive_menu'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не может видеть неопубликованное меню"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_some_user(self):
        """Авторизованный пользователь не может видеть неопубликованное меню"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_cheap_worker(self):
        """Работник дешевого ресторана просматривает неопубликованное меню своего ресторана"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_inactive_menu(ans.json())

    def test_cheap_owner(self):
        """Хозяин дешевого ресторана просматривает неопубликованное меню своего ресторана"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_inactive_menu(ans.json())

    def test_premium_worker(self):
        """Работник ресторана не может видеть неопубликованное меню другого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_premium_owner(self):
        """Хозяин ресторана не может видеть неопубликованное меню другого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_admin(self):
        """Администратор просматривает неопубликованное меню"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_cheap_inactive_menu(ans.json())


class MenuCreateTest(BaseTestCase):
    """
    Тесты для создания нового меню для премиум-ресторана
    """

    def __get_url(self):
        return "/api/v1/menu/"

    def __post_new_menu_data(self):
        """
        Выполнить POST-запрос для создания нового меню для премиум-ресторана
        и вернуть ответ на этот запрос.
        """
        return self.client.post(
            self.__get_url(),
            {
                'restaurant': self._data['premium_restaurant'].pk,
                'translations': {
                    'en': {'title': "New menu"}
                },
                'published': True
            },
            format='json'
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может загружать новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)

    def test_some_user(self):
        """Произвольный пользователь не может загружать новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('some_user'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
