"""
Тесты для обработчиков входа пользователя в систему и выхода пользователя
из системы
"""

from users.models import User
from restaurants.tests._fixtures import BaseTestCase


class TestRegister(BaseTestCase):
    """
    Тесты для регистрации пользователя в системе.
    """

    def __get_url(self):
        return "/api/v1/users/register/"

    def test_registration(self):
        """Успешная регистрация пользователя в системе"""
        ans = self.client.post(
            self.__get_url(),
            {
                'username': 'new_user',
                'password': 'new_password',
                'email': 'new_user@localhost',
                'phone': '+79109876543'
            },
            format='json'
        )
        self.assertEqual(ans.status_code, 201)
        info = ans.json()
        self.assertCountEqual(info.keys(), ['id', 'username', 'email', 'phone'])
        pk = info['id']
        self.assertEqual(info['username'], 'new_user')
        self.assertEqual(info['email'], 'new_user@localhost')
        self.assertEqual(info['phone'], '+79109876543')
        # Проверить, что новый пользователь был создан
        new_user = User.objects.get(pk=pk)
        self.assertEqual(new_user.username, 'new_user')
        self.assertEqual(new_user.email, 'new_user@localhost')
        self.assertEqual(new_user.phone, '+79109876543')
        # И что от его имени можно войти, но он не имеет полномочий
        self.assertEqual(new_user.is_active, True)
        self.assertEqual(new_user.is_staff, False)
        self.assertEqual(new_user.is_superuser, False)
