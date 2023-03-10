"""
Тесты для обработчиков входа пользователя в систему и выхода пользователя
из системы
"""

from django.utils.translation import gettext_lazy as _

from restaurants.tests._fixtures import BaseTestCase


class TestLogin(BaseTestCase):
    """
    Тесты для входа пользователя в систему.
    """

    def __get_url(self):
        return "/api/v1/users/login/"

    def test_no_password(self):
        """Нельзя войти без пароля"""
        ans = self.client.post(self.__get_url(), {'username': "some_user"})
        self.assertEqual(ans.status_code, 400)
        self.assertEqual(
            ans.json(), {'detail': _("Username and password must be provided")}
        )

    def test_invalid_password(self):
        """Нельзя войти с неправильным паролем"""
        ans = self.client.post(
            self.__get_url(), {'username': "some_user", 'password': "123"}
        )
        self.assertEqual(ans.status_code, 403)
        self.assertEqual(
            ans.json(), {'detail': _("Incorrect username or password")}
        )

    def test_banned_user(self):
        """Пользователь со сброшенным флагом is_active войти не может"""
        self._data['some_user'].is_active = False
        self._data['some_user'].save()
        ans = self.client.post(
            self.__get_url(), {'username': "some_user", 'password': "some_user"}
        )
        self.assertEqual(ans.status_code, 403)
        self.assertEqual(
            ans.json(), {'detail': _("Incorrect username or password")}
        )
        self._data['some_user'].is_active = True
        self._data['some_user'].save()

    def test_login(self):
        """Успешный вход в систему"""
        ans = self.client.get(f"/api/v1/menu_courses/{self._data['disabled_water'].pk}/")
        self.assertEqual(ans.status_code, 404)
        ans = self.client.post(
            self.__get_url(), {'username': "cheap_worker", 'password': "cheap_worker"}
        )
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['detail', 'user', 'token'])
        self.assertEqual(info['user'], self._data['cheap_worker'].pk)
        self.assertEqual(info['detail'], _("Successfully logged in"))
        # Проверить, что токен работает, обратившись к неопубликованному
        # блюду дешевого ресторана
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {info['token']}")
        ans = self.client.get(f"/api/v1/menu_courses/{self._data['disabled_water'].pk}/")
        self.assertEqual(ans.status_code, 200)

    def test_login_logout(self):
        """Успешный вход в систему и выход из нее"""
        ans = self.client.get(f"/api/v1/menu_courses/{self._data['disabled_water'].pk}/")
        self.assertEqual(ans.status_code, 404)
        ans = self.client.post(
            self.__get_url(), {'username': "cheap_worker", 'password': "cheap_worker"}
        )
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['detail', 'user', 'token'])
        self.assertEqual(info['user'], self._data['cheap_worker'].pk)
        self.assertEqual(info['detail'], _("Successfully logged in"))
        # Проверить, что токен работает, обратившись к неопубликованному
        # блюду дешевого ресторана
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {info['token']}")
        ans = self.client.get(f"/api/v1/menu_courses/{self._data['disabled_water'].pk}/")
        self.assertEqual(ans.status_code, 200)
        # Выйти из системы
        ans = self.client.post("/api/v1/users/logout/", {})
        self.assertEqual(ans.status_code, 200)
        self.assertEqual(ans.json(), {'detail': _("Successfully logged out")})
        # Проверить что токен теперь не работает
        ans = self.client.get(f"/api/v1/menu_courses/{self._data['disabled_water'].pk}/")
        self.assertEqual(ans.status_code, 401)
