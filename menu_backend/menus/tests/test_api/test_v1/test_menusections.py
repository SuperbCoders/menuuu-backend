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
        """Неавторизованный пользователь просматривает список разделов опубликованных меню"""
        ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_published_sections(info)

    def test_some_user(self):
        """Авторизованный пользователь просматривает список разделов опубликованных меню"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_published_sections(info)

    def test_cheap_worker(self):
        """Сотрудник ресторана видит также и разделы неопубликованных меню своего ресторана"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_all_sections(info)

    def test_cheap_owner(self):
        """Хозяин ресторана видит также и разделы неопубликованных меню своего ресторана"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_all_sections(info)

    def test_premium_worker(self):
        """Работник ресторана не видит раздел чужого неопубликованного меню"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_published_sections(info)

    def test_premium_owner(self):
        """Хозяин ресторана не видит раздел чужого неопубликованного меню"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_published_sections(info)

    def test_admin(self):
        """Администратор видит все разделы всех меню, в том числе неопубликованных"""
        with self.logged_in('admin'):
            ans = self.client.get(self.URL)
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_all_sections(info)


class PublishedMenuSectionRetrieveTest(BaseTestCase):
    """
    Тесты для API получения одиночного раздела опубликованного меню.
    Эта возможность должна быть доступна всем пользователям, включая
    неавторизованных.
    """

    def __get_url(self):
        return f"/api/v1/menu_sections/{self._data['drinks_section'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает раздел меню"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_drinks_section(ans.json())

    def test_some_user(self):
        """Авторизованный пользователь просматривает раздел меню"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_drinks_section(ans.json())

    def test_cheap_worker(self):
        """Работник ресторана просматривает раздел меню"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_drinks_section(ans.json())

    def test_cheap_owner(self):
        """Хозяин ресторана просматривает раздел меню"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_drinks_section(ans.json())
