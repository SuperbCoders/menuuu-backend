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


class RestaurantStaffUpdateTest(BaseTestCase):
    """
    Тесты для API изменения данных о должности работника в ресторане
    """

    def __get_url(self):
        staff = self._data['cheap_worker'].restaurant_staff.first()
        return f"/api/v1/restaurant_staff/{staff.pk}/"

    def __put_new_restaurant_staff(self):
        """
        Выполнить PUT запрос на изменение должности одного из работников ресторана
        на владельца
        """
        return self.client.put(
            self.__get_url(),
            {
                'position': 'owner',
                'user': self._data['cheap_worker'].pk,
                'restaurant': self._data['cheap_restaurant'].pk
            },
            format='json'
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может изменить должность работника"""
        ans = self.__put_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_some_user(self):
        """Зарегистрированный пользователь не может изменить должность работника"""
        with self.logged_in('some_user'):
            ans = self.__put_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_cheap_worker(self):
        """Работник не может изменить свою должность"""
        with self.logged_in('cheap_worker'):
            ans = self.__put_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_cheap_owner(self):
        """Хозяин ресторана делает работника совладельцем"""
        with self.logged_in('cheap_owner'):
            ans = self.__put_new_restaurant_staff()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что должность работника изменилась как надо
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "owner"
        )

    def test_premium_worker(self):
        """Работник не может изменить должность работника чужого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.__put_new_restaurant_staff()
        self.assertEqual(ans.status_code, 404)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_premium_owner(self):
        """Вдаделец не может изменить должность работника чужого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.__put_new_restaurant_staff()
        self.assertEqual(ans.status_code, 404)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_admin(self):
        """Администратор делает работника ресторана совладельцем"""
        with self.logged_in('admin'):
            ans = self.__put_new_restaurant_staff()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что должность работника изменилась как надо
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "owner"
        )


class RestaurantStaffPartialUpdateTest(BaseTestCase):
    """
    Тесты для API частичного изменения данных о должности работника в ресторане
    """

    def __get_url(self):
        staff = self._data['cheap_worker'].restaurant_staff.first()
        return f"/api/v1/restaurant_staff/{staff.pk}/"

    def __patch_new_restaurant_staff(self):
        """
        Выполнить PUT запрос на изменение должности одного из работников ресторана
        на владельца
        """
        return self.client.patch(
            self.__get_url(),
            {
                'position': 'owner',
                'user': self._data['cheap_worker'].pk,
                'restaurant': self._data['cheap_restaurant'].pk
            },
            format='json'
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может изменить должность работника"""
        ans = self.__patch_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_some_user(self):
        """Зарегистрированный пользователь не может изменить должность работника"""
        with self.logged_in('some_user'):
            ans = self.__patch_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_cheap_worker(self):
        """Работник не может изменить свою должность"""
        with self.logged_in('cheap_worker'):
            ans = self.__patch_new_restaurant_staff()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_cheap_owner(self):
        """Хозяин ресторана делает работника совладельцем"""
        with self.logged_in('cheap_owner'):
            ans = self.__patch_new_restaurant_staff()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что должность работника изменилась как надо
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "owner"
        )

    def test_premium_worker(self):
        """Работник не может изменить должность работника чужого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.__patch_new_restaurant_staff()
        self.assertEqual(ans.status_code, 404)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_premium_owner(self):
        """Вдаделец не может изменить должность работника чужого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.__patch_new_restaurant_staff()
        self.assertEqual(ans.status_code, 404)
        # Проверяем, что должность работника не изменилась
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_admin(self):
        """Администратор делает работника ресторана совладельцем"""
        with self.logged_in('admin'):
            ans = self.__patch_new_restaurant_staff()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что должность работника изменилась как надо
        self.assertEqual(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "owner"
        )


class RestaurantStaffDeleteTest(BaseTestCase):
    """
    Тесты для API удаления данных о должности работника в ресторане
    """

    def __get_url(self):
        staff = self._data['cheap_worker'].restaurant_staff.first()
        return f"/api/v1/restaurant_staff/{staff.pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не может уволить работника"""
        ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertTrue(self._data['cheap_worker'].restaurant_staff.exists())
        self.assertTrue(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_some_user(self):
        """Зарегистрированный пользователь не может уволить работника"""
        with self.logged_in('some_user'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertTrue(self._data['cheap_worker'].restaurant_staff.exists())
        self.assertTrue(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_cheap_worker(self):
        """Работник не может отменить свое место работы сам"""
        with self.logged_in('cheap_worker'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что должность работника не изменилась
        self.assertTrue(self._data['cheap_worker'].restaurant_staff.exists())
        self.assertTrue(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_cheap_owner(self):
        """Хозяин ресторана увольняет работника"""
        with self.logged_in('cheap_owner'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 204)
        # Проверяем, что работник больше не числится в ресторане
        self.assertFalse(self._data['cheap_worker'].restaurant_staff.exists())

    def test_premium_worker(self):
        """Работник не может уволить работника чужого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 404)
        # Проверяем, что должность работника не изменилась
        self.assertTrue(self._data['cheap_worker'].restaurant_staff.exists())
        self.assertTrue(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_premium_owner(self):
        """Владелец не может уволить работника чужого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 404)
        # Проверяем, что должность работника не изменилась
        self.assertTrue(self._data['cheap_worker'].restaurant_staff.exists())
        self.assertTrue(
            self._data['cheap_worker'].restaurant_staff.first().position,
            "worker"
        )

    def test_admin(self):
        """Администратор убирает должность работника в ресторане"""
        with self.logged_in('admin'):
            ans = self.client.delete(self.__get_url())
        self.assertEqual(ans.status_code, 204)
        # Проверяем, что работник больше не числится в ресторане
        self.assertFalse(self._data['cheap_worker'].restaurant_staff.exists())


class RestaurantStaffUserFilterTest(BaseTestCase):
    """
    Тесты для API получения списка всех работников ресторанов, с фильтрацией по
    пользователю
    """

    def __get_url(self):
        return f"/api/v1/restaurant_staff/?user={self._data['cheap_worker'].pk}"

    def __verify_cheap_worker(self, info):
        """
        Проверить, что словарь info содержит корректую информацию о должности
        работника cheap_worker в своем ресторане
        """
        self.assertEqual(info['position'], "worker")
        self.assertEqual(info['restaurant'], self._data['cheap_restaurant'].pk)
        self.assertEqual(info['user'], self._data['cheap_worker'].pk)

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
        """Сотрудник ресторана видит собственную должность"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 1)
        self.__verify_cheap_worker(results[0])

    def test_cheap_owner(self):
        """Хозяин ресторана видит должности своего сотрудника"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 1)
        self.__verify_cheap_worker(results[0])

    def test_premium_worker(self):
        """Сотрудник ресторана не видит сотрудников чужого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 0)

    def test_premium_owner(self):
        """Хозяин ресторана видит не видит сотрудников чужого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 0)

    def test_admin(self):
        """Администратор видит список должностей пользователя в ресторанах"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 1)
        self.__verify_cheap_worker(results[0])


class RestaurantStaffRestaurantFilterTest(BaseTestCase):
    """
    Тесты для API получения списка всех работников ресторанов, с фильтрацией по
    ресторану
    """

    def __get_url(self):
        return f"/api/v1/restaurant_staff/?restaurant={self._data['cheap_restaurant'].pk}"

    def __verify_cheap_worker(self, info):
        """
        Проверить, что словарь info содержит корректую информацию о должности
        работника cheap_worker в своем ресторане
        """
        self.assertEqual(info['position'], "worker")
        self.assertEqual(info['restaurant'], self._data['cheap_restaurant'].pk)
        self.assertEqual(info['user'], self._data['cheap_worker'].pk)

    def __verify_cheap_owner(self, info):
        """
        Проверить, что словарь info содержит корректую информацию о должности
        работника cheap_owner в своем ресторане
        """
        self.assertEqual(info['position'], "owner")
        self.assertEqual(info['restaurant'], self._data['cheap_restaurant'].pk)
        self.assertEqual(info['user'], self._data['cheap_owner'].pk)

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
        """Сотрудник ресторана видит собственную должность и должность руководителя"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 2)
        if results[0]['position'] == 'worker':
            self.__verify_cheap_worker(results[0])
            self.__verify_cheap_owner(results[1])
        elif results[0]['position'] == 'owner':
            self.__verify_cheap_owner(results[0])
            self.__verify_cheap_worker(results[1])
        else:
            self.fail(f"Неизвестная должность работника {results[0]['position']}")

    def test_cheap_owner(self):
        """Владелец ресторана видит собственную должность и должность подчиненного"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 2)
        if results[0]['position'] == 'worker':
            self.__verify_cheap_worker(results[0])
            self.__verify_cheap_owner(results[1])
        elif results[0]['position'] == 'owner':
            self.__verify_cheap_owner(results[0])
            self.__verify_cheap_worker(results[1])
        else:
            self.fail(f"Неизвестная должность работника {results[0]['position']}")

    def test_premium_worker(self):
        """Сотрудник ресторана не видит сотрудников другого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        # Список возвращается, но он будет пуст
        results = ans.json()['results']
        self.assertEqual(len(results), 0)

    def test_premium_owner(self):
        """Хозяин ресторана не видит сотрудников другого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        # Список возвращается, но он будет пуст
        results = ans.json()['results']
        self.assertEqual(len(results), 0)

    def test_admin(self):
        """Администратор видит всех работников целевого ресторана"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        results = ans.json()['results']
        self.assertEqual(len(results), 2)
        if results[0]['position'] == 'worker':
            self.__verify_cheap_worker(results[0])
            self.__verify_cheap_owner(results[1])
        elif results[0]['position'] == 'owner':
            self.__verify_cheap_owner(results[0])
            self.__verify_cheap_worker(results[1])
        else:
            self.fail(f"Неизвестная должность работника {results[0]['position']}")
