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

    def test_cheap_worker(self):
        """Сотрудник ресторана видит список сотрудников своего ресторана"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 2)
        self.assertCountEqual(
            [item['position'] for item in results],
            ['owner', 'worker']
        )
        self.assertCountEqual(
            [item['restaurant'] for item in results],
            [self._data['cheap_restaurant'].pk, self._data['cheap_restaurant'].pk]
        )
        self.assertCountEqual(
            [item['user'] for item in results],
            [self._data['cheap_worker'].pk, self._data['cheap_owner'].pk]
        )

    def test_cheap_owner(self):
        """Хозяин ресторана видит список сотрудников своего ресторана"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 2)
        self.assertCountEqual(
            [item['position'] for item in results],
            ['owner', 'worker']
        )
        self.assertCountEqual(
            [item['restaurant'] for item in results],
            [self._data['cheap_restaurant'].pk, self._data['cheap_restaurant'].pk]
        )
        self.assertCountEqual(
            [item['user'] for item in results],
            [self._data['cheap_worker'].pk, self._data['cheap_owner'].pk]
        )

    def test_premium_worker(self):
        """Сотрудник ресторана видит список сотрудников своего ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 2)
        self.assertCountEqual(
            [item['position'] for item in results],
            ['owner', 'worker']
        )
        self.assertCountEqual(
            [item['restaurant'] for item in results],
            [self._data['premium_restaurant'].pk, self._data['premium_restaurant'].pk]
        )
        self.assertCountEqual(
            [item['user'] for item in results],
            [self._data['premium_worker'].pk, self._data['premium_owner'].pk]
        )

    def test_premium_owner(self):
        """Хозяин ресторана видит список сотрудников своего ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 2)
        self.assertCountEqual(
            [item['position'] for item in results],
            ['owner', 'worker']
        )
        self.assertCountEqual(
            [item['restaurant'] for item in results],
            [self._data['premium_restaurant'].pk, self._data['premium_restaurant'].pk]
        )
        self.assertCountEqual(
            [item['user'] for item in results],
            [self._data['premium_worker'].pk, self._data['premium_owner'].pk]
        )

    def test_admin(self):
        """Администратор видит список всех сотрудников всех ресторанов"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 4)
        self.assertCountEqual(
            [item['position'] for item in results],
            ['owner', 'worker', 'owner', 'worker']
        )
        self.assertCountEqual(
            [item['restaurant'] for item in results],
            [
                self._data['premium_restaurant'].pk, self._data['premium_restaurant'].pk,
                self._data['cheap_restaurant'].pk, self._data['cheap_restaurant'].pk
            ]
        )
        self.assertCountEqual(
            [item['user'] for item in results],
            [
                self._data['premium_worker'].pk, self._data['premium_owner'].pk,
                self._data['cheap_worker'].pk, self._data['cheap_owner'].pk
            ]
        )


class RestaurantStaffRetrieveTest(BaseTestCase):
    """
    Тесты для API получения данных об определенном работнике ресторана
    """

    def __get_url(self):
        staff = self._data['cheap_worker'].restaurant_staff.first()
        return f"/api/v1/restaurant_staff/{staff.pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не видит запись о сотруднике ресторана"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 403)

    def test_some_user(self):
        """Пользователь без работы не видит запись о сотруднике ресторана"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 403)

    def test_cheap_worker(self):
        """Работник первого ресторана видит свое место работы"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['user'], self._data['cheap_worker'].pk)
        self.assertEqual(info['restaurant'], self._data['cheap_restaurant'].pk)
        self.assertEqual(info['position'], "worker")

    def test_cheap_owner(self):
        """Хозяин первого ресторана видит своего работника"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['user'], self._data['cheap_worker'].pk)
        self.assertEqual(info['restaurant'], self._data['cheap_restaurant'].pk)
        self.assertEqual(info['position'], "worker")

    def test_premium_worker(self):
        """Работник ресторана не видит работников другого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        # Код ответа будет 404 вместо 403, так как целевой объект
        # не входит в список видимых для этого пользователя
        self.assertEqual(ans.status_code, 404)

    def test_premium_owner(self):
        """Хозяин ресторана не видит работников другого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        # Код ответа будет 404 вместо 403, так как целевой объект
        # не входит в список видимых для этого пользователя
        self.assertEqual(ans.status_code, 404)

    def test_admin(self):
        """Администратор видит должности пользователей во всех ресторанах"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['user'], self._data['cheap_worker'].pk)
        self.assertEqual(info['restaurant'], self._data['cheap_restaurant'].pk)
        self.assertEqual(info['position'], "worker")


class RestaurantStaffCreateTest(BaseTestCase):
    """
    Тесты для API создания новых должностей пользователей в ресторанах
    """

    def __get_url(self):
        return "/api/v1/restaurant_staff/"

    def __post_new_restaurant_staff(self):
        """
        Выполнить POST запрос на прием в ресторан нового работника и вернуть
        результат
        """
        return self.client.post(
            self.__get_url(),
            {
                'position': 'worker',
                'user': self._data['some_user'].pk,
                'restaurant': self._data['cheap_restaurant'].pk
            },
            format='json'
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может добавить в ресторан нового сотрудника"""
        ans = self.__post_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Новый работник не был добавлен - проверяем это
        self.assertFalse(self._data['some_user'].restaurant_staff.exists())

    def test_some_user(self):
        """Пользователь без полномочий не может добавить в ресторан нового сотрудника"""
        with self.logged_in('some_user'):
            ans = self.__post_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Новый работник не был добавлен - проверяем это
        self.assertFalse(self._data['some_user'].restaurant_staff.exists())

    def test_cheap_worker(self):
        """Работник ресторана не может добавить в ресторан нового сотрудника"""
        with self.logged_in('cheap_worker'):
            ans = self.__post_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Новый работник не был добавлен - проверяем это
        self.assertFalse(self._data['some_user'].restaurant_staff.exists())

    def test_cheap_owner(self):
        """Владелец добавляет в свой ресторан нового работника"""
        with self.logged_in('cheap_owner'):
            ans = self.__post_new_restaurant_staff()
        self.assertEqual(ans.status_code, 201)
        # Новый работник был добавлен
        self.assertTrue(
            self._data['cheap_restaurant'].restaurant_staff.filter(
                user=self._data['some_user'], position='worker'
            ).exists()
        )

    def test_premium_worker(self):
        """Работник ресторана не может добавить в другой ресторан нового сотрудника"""
        with self.logged_in('premium_worker'):
            ans = self.__post_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Новый работник не был добавлен - проверяем это
        self.assertFalse(self._data['some_user'].restaurant_staff.exists())

    def test_premium_owner(self):
        """Хозяин ресторана не может добавить в другой ресторан нового сотрудника"""
        with self.logged_in('premium_owner'):
            ans = self.__post_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Новый работник не был добавлен - проверяем это
        self.assertFalse(self._data['some_user'].restaurant_staff.exists())

    def test_admin(self):
        """Администратор добавляет в ресторан нового работника"""
        with self.logged_in('admin'):
            ans = self.__post_new_restaurant_staff()
        self.assertEqual(ans.status_code, 201)
        # Новый работник был добавлен
        self.assertTrue(
            self._data['cheap_restaurant'].restaurant_staff.filter(
                user=self._data['some_user'], position='worker'
            ).exists()
        )
