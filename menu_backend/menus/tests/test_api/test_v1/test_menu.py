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


class ActiveMenuCreateTest(BaseTestCase):
    """
    Тесты для создания нового опубликованного меню для премиум-ресторана.
    Право это делать имеет только владелец и работник премиум-ресторана
    а также администратор. При успешном добавлении нового меню старое
    должно остаться, но стать неопубликованным.
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
        self.assertEqual(ans.status_code, 401)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

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
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_cheap_worker(self):
        """Работник ресторана не может загружать новое меню для другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_worker'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_cheap_owner(self):
        """Хозяин ресторана не может загружать новое меню для другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_premium_worker(self):
        """Работник ресторана загружает для своего ресторана новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_worker'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 201)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 4)
        # И что старое меню премиум-ресторана теперь неактивно
        self.assertFalse(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)
        # И что новое меню активно и правильно называется
        new_pk = ans.json()['id']
        new_menu = Menu.objects.get(pk=new_pk)
        self.assertTrue(new_menu.published)
        self.assertEqual(new_menu.title, "New menu")
        self.assertEqual(new_menu.restaurant.pk, self._data['premium_restaurant'].pk)

    def test_premium_owner(self):
        """Владелец ресторана загружает для своего ресторана новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_owner'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 201)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 4)
        # И что старое меню премиум-ресторана теперь неактивно
        self.assertFalse(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)
        # И что новое меню активно и правильно называется
        new_pk = ans.json()['id']
        new_menu = Menu.objects.get(pk=new_pk)
        self.assertTrue(new_menu.published)
        self.assertEqual(new_menu.title, "New menu")
        self.assertEqual(new_menu.restaurant.pk, self._data['premium_restaurant'].pk)

    def test_admin(self):
        """Администратор загружает для ресторана новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('admin'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 201)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 4)
        # И что старое меню премиум-ресторана теперь неактивно
        self.assertFalse(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)
        # И что новое меню активно и правильно называется
        new_pk = ans.json()['id']
        new_menu = Menu.objects.get(pk=new_pk)
        self.assertTrue(new_menu.published)
        self.assertEqual(new_menu.title, "New menu")
        self.assertEqual(new_menu.restaurant.pk, self._data['premium_restaurant'].pk)


class InactiveMenuCreateTest(BaseTestCase):
    """
    Тесты для создания нового неопубликованного меню для премиум-ресторана.
    Право это делать имеет только владелец и работник премиум-ресторана
    а также администратор. При успешном добавлении нового меню старое
    должно оставаться активным, а новое - быть неактивным.
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
                'published': False
            },
            format='json'
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может загружать новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 401)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

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
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_cheap_worker(self):
        """Работник ресторана не может загружать новое меню для другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_worker'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_cheap_owner(self):
        """Хозяин ресторана не может загружать новое меню для другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_premium_worker(self):
        """Работник ресторана загружает для своего ресторана новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_worker'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 201)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 4)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)
        # И что новое меню правильно называется и что оно неактивно
        new_pk = ans.json()['id']
        new_menu = Menu.objects.get(pk=new_pk)
        self.assertFalse(new_menu.published)
        self.assertEqual(new_menu.title, "New menu")
        self.assertEqual(new_menu.restaurant.pk, self._data['premium_restaurant'].pk)

    def test_premium_owner(self):
        """Хозяин ресторана загружает для своего ресторана новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_owner'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 201)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 4)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)
        # И что новое меню правильно называется и что оно неактивно
        new_pk = ans.json()['id']
        new_menu = Menu.objects.get(pk=new_pk)
        self.assertFalse(new_menu.published)
        self.assertEqual(new_menu.title, "New menu")
        self.assertEqual(new_menu.restaurant.pk, self._data['premium_restaurant'].pk)

    def test_admin(self):
        """Администратор загружает новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('admin'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 201)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 4)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)
        # И что новое меню правильно называется и что оно неактивно
        new_pk = ans.json()['id']
        new_menu = Menu.objects.get(pk=new_pk)
        self.assertFalse(new_menu.published)
        self.assertEqual(new_menu.title, "New menu")
        self.assertEqual(new_menu.restaurant.pk, self._data['premium_restaurant'].pk)


class IncorrectMenuCreateTest(BaseTestCase):
    """
    Тесты попытки создать новое меню не указывая ресторан. Это не должно
    получаться и не должно приводить к каким-либо изменениям меню
    """

    def __get_url(self):
        return "/api/v1/menu/"

    def __post_new_menu_data(self):
        """
        Выполнить POST-запрос для создания нового меню
        """
        return self.client.post(
            self.__get_url(),
            {
                'translations': {
                    'en': {'title': "New menu"}
                },
                'published': False
            },
            format='json'
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может загружать новое меню"""
        self.assertEqual(Menu.objects.count(), 3)
        ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 401)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню обоих ресторанов все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

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
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_cheap_worker(self):
        """Работник ресторана не может загружать некорректное меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_worker'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_cheap_owner(self):
        """Хозяин ресторана не может загружать некорректное меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_premium_worker(self):
        """Работник ресторана не может загружать некорректное меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_worker'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_premium_owner(self):
        """Хозяин ресторана не может загружать некорректное меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_owner'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_admin(self):
        """Администратор не может загружать некорректное меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('admin'):
            ans = self.__post_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что новое меню не было добавлено
        self.assertEqual(Menu.objects.count(), 3)
        # И что старое меню премиум-ресторана все еще активно
        self.assertTrue(Menu.objects.get(pk=self._data['premium_menu'].pk).published)
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)


class MenuUpdateTest(BaseTestCase):
    """
    Тесты для API изменения меню
    """

    def __get_url(self):
        return f"/api/v1/menu/{self._data['cheap_menu'].pk}/"

    def __put_new_menu_data(self):
        """
        Выполнить PUT-запрос для обновления меню и вернуть результат
        """
        return self.client.put(
            self.__get_url(),
            {
                'restaurant': self._data['cheap_restaurant'].pk,
                'translations': {
                    'en': {'title': "Updated menu"},
                    'ru': {'title': "Обновленное меню"},
                },
                'published': True
            },
            format='json'
        )

    def __verify_cheap_menu_unchanged(self):
        """Проверить что меню фастфуд-ресторана не было изменено"""
        menu = Menu.objects.get(pk=self._data['cheap_menu'].pk)
        self.assertTrue(menu.published)
        self.assertEqual(menu.restaurant.pk, self._data['cheap_restaurant'].pk)
        self.assertEqual(menu.title, "Menu")
        menu.set_current_language('ru')
        self.assertEqual(menu.title, "Меню")

    def __verify_cheap_menu_changed(self):
        """Проверить что меню фастфуд-ресторана было изменено"""
        menu = Menu.objects.get(pk=self._data['cheap_menu'].pk)
        self.assertTrue(menu.published)
        self.assertEqual(menu.restaurant.pk, self._data['cheap_restaurant'].pk)
        self.assertEqual(menu.title, "Updated menu")
        menu.set_current_language('ru')
        self.assertEqual(menu.title, "Обновленное меню")

    def test_unauthorized(self):
        """Неавторизованный пользователь не редактировать меню"""
        self.assertEqual(Menu.objects.count(), 3)
        ans = self.__put_new_menu_data()
        self.assertEqual(ans.status_code, 401)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_some_user(self):
        """Авторизованный пользователь не редактировать меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('some_user'):
            ans = self.__put_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_cheap_worker(self):
        """Работник ресторана редактирует меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_worker'):
            ans = self.__put_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_changed()

    def test_cheap_owner(self):
        """Хозяин ресторана редактирует меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.__put_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_changed()

    def test_premium_worker(self):
        """Работник ресторана не может редактировать меню чужого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_worker'):
            ans = self.__put_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не изменилось
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_premium_owner(self):
        """Хозяин ресторана не может редактировать меню чужого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_owner'):
            ans = self.__put_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не изменилось
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_admin(self):
        """Администратор редактирует меню ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('admin'):
            ans = self.__put_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_changed()


class MenuPartialUpdateTest(BaseTestCase):
    """
    Тесты для API частичного изменения меню методом PATCH
    """

    def __get_url(self):
        return f"/api/v1/menu/{self._data['cheap_menu'].pk}/"

    def __patch_new_menu_data(self):
        """
        Выполнить PATCH-запрос для обновления меню и вернуть результат
        """
        return self.client.patch(
            self.__get_url(),
            {
                'published': False
            },
            format='json'
        )

    def __verify_cheap_menu_unchanged(self):
        """Проверить что меню фастфуд-ресторана не было изменено"""
        menu = Menu.objects.get(pk=self._data['cheap_menu'].pk)
        self.assertTrue(menu.published)
        self.assertEqual(menu.restaurant.pk, self._data['cheap_restaurant'].pk)
        self.assertEqual(menu.title, "Menu")
        menu.set_current_language('ru')
        self.assertEqual(menu.title, "Меню")

    def __verify_cheap_menu_changed(self):
        """Проверить что у меню фастфуд-ресторана был сброшен флаг активности"""
        menu = Menu.objects.get(pk=self._data['cheap_menu'].pk)
        self.assertFalse(menu.published)
        self.assertEqual(menu.restaurant.pk, self._data['cheap_restaurant'].pk)
        self.assertEqual(menu.title, "Menu")
        menu.set_current_language('ru')
        self.assertEqual(menu.title, "Меню")

    def test_unauthorized(self):
        """Неавторизованный пользователь не может редактировать меню"""
        self.assertEqual(Menu.objects.count(), 3)
        ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 401)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_some_user(self):
        """Авторизованный пользователь не может редактировать меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('some_user'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_cheap_worker(self):
        """Работник ресторана редактирует меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_worker'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_changed()

    def test_cheap_owner(self):
        """Хозяин ресторана редактирует меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_changed()

    def test_premium_worker(self):
        """Работник ресторана не может редактировать меню чужого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_worker'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не изменилось
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_premium_owner(self):
        """Хозяин ресторана не может редактировать меню чужого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_owner'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не изменилось
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_unchanged()

    def test_admin(self):
        """Администратор редактирует меню ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('admin'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_cheap_menu_changed()


class InactiveMenuPartialUpdateTest(BaseTestCase):
    """
    Тесты для API частичного изменения неактивного меню методом PATCH. Этому меню
    выставляется флаг активности в True что должно привести к сбросу флага активности
    другого меню того же ресторана в False.
    """

    def __get_url(self):
        return f"/api/v1/menu/{self._data['inactive_menu'].pk}/"

    def __patch_new_menu_data(self):
        """
        Выполнить PATCH-запрос для обновления меню и вернуть результат
        """
        return self.client.patch(
            self.__get_url(),
            {
                'published': True
            },
            format='json'
        )

    def __verify_inactive_menu_unchanged(self):
        """Проверить что меню фастфуд-ресторана не было изменено"""
        self.assertTrue(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)
        self.assertFalse(Menu.objects.get(pk=self._data['inactive_menu'].pk).published)

    def __verify_inactive_menu_changed(self):
        """Проверить что у меню фастфуд-ресторана теперь опубликовано другое меню"""
        self.assertTrue(Menu.objects.get(pk=self._data['inactive_menu'].pk).published)
        self.assertFalse(Menu.objects.get(pk=self._data['cheap_menu'].pk).published)

    def test_unauthorized(self):
        """Неавторизованный пользователь не может переключать текущее меню"""
        self.assertEqual(Menu.objects.count(), 3)
        ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 401)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_inactive_menu_unchanged()

    def test_some_user(self):
        """Авторизованный пользователь не может переключать текущее меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('some_user'):
            ans = self.__patch_new_menu_data()
        # Статус 403, так как пользователь не может применять к меню метод PATCH
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_inactive_menu_unchanged()

    def test_cheap_worker(self):
        """Работник ресторана переключает текущее меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_worker'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_inactive_menu_changed()

    def test_cheap_owner(self):
        """Хозяин ресторана переключает текущее меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_inactive_menu_changed()

    def test_premium_worker(self):
        """Работник ресторана не может переключать текущее меню другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_worker'):
            ans = self.__patch_new_menu_data()
        # Статус 404 а не 403, так как если меню неопубликовано, то для
        # посторонних оно как бы не существует
        self.assertEqual(ans.status_code, 404)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_inactive_menu_unchanged()

    def test_premium_owner(self):
        """Хозяин ресторана не может переключать текущее меню другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_owner'):
            ans = self.__patch_new_menu_data()
        # Статус 404 а не 403, так как если меню неопубликовано, то для
        # посторонних оно как бы не существует
        self.assertEqual(ans.status_code, 404)
        # Проверить, что меню не было изменено
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_inactive_menu_unchanged()

    def test_admin(self):
        """Администратор переключает текущее меню ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('admin'):
            ans = self.__patch_new_menu_data()
        self.assertEqual(ans.status_code, 200)
        # Проверить, что меню изменилось как надо
        self.assertEqual(Menu.objects.count(), 3)
        self.__verify_inactive_menu_changed()


class MenuDeleteTest(BaseTestCase):
    """
    Тесты для API удаления меню
    ---------------------------

    Удаляет неактивное меню дешевого ресторана. Сделать это могут только сотрудник
    или владелец дешевого ресторана либо администратор.
    """

    def __get_url(self):
        return f"/api/v1/menu/{self._data['inactive_menu'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не может удалить меню"""
        self.assertEqual(Menu.objects.count(), 3)
        ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 401)
        # Проверить, что меню не было удалено
        self.assertEqual(Menu.objects.count(), 3)
        self.assertTrue(Menu.objects.filter(pk=self._data['inactive_menu'].pk).exists())

    def test_some_user(self):
        """Авторизованный пользователь не может удалить меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('some_user'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 403)
        # Проверить, что меню не было удалено
        self.assertEqual(Menu.objects.count(), 3)
        self.assertTrue(Menu.objects.filter(pk=self._data['inactive_menu'].pk).exists())

    def test_cheap_worker(self):
        """Работник ресторана удаляет меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_worker'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 204)
        # Проверить, что меню удалено
        self.assertEqual(Menu.objects.count(), 2)
        self.assertFalse(Menu.objects.filter(pk=self._data['inactive_menu'].pk).exists())

    def test_cheap_owner(self):
        """Хозяин ресторана удаляет меню своего ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 204)
        # Проверить, что меню удалено
        self.assertEqual(Menu.objects.count(), 2)
        self.assertFalse(Menu.objects.filter(pk=self._data['inactive_menu'].pk).exists())

    def test_premium_worker(self):
        """Работник ресторана не может удалить меню другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_worker'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 404)
        # Проверить, что меню не было удалено
        self.assertEqual(Menu.objects.count(), 3)
        self.assertTrue(Menu.objects.filter(pk=self._data['inactive_menu'].pk).exists())

    def test_premium_owner(self):
        """Хозяин ресторана не может удалить меню другого ресторана"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('premium_owner'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 404)
        # Проверить, что меню не было удалено
        self.assertEqual(Menu.objects.count(), 3)
        self.assertTrue(Menu.objects.filter(pk=self._data['inactive_menu'].pk).exists())

    def test_admin(self):
        """Администратор удаляет меню"""
        self.assertEqual(Menu.objects.count(), 3)
        with self.logged_in('cheap_owner'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 204)
        # Проверить, что меню удалено
        self.assertEqual(Menu.objects.count(), 2)
        self.assertFalse(Menu.objects.filter(pk=self._data['inactive_menu'].pk).exists())
