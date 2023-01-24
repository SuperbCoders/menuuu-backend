"""
Тесты для стандартных REST API для работы с ресторанами
"""

from restaurants.tests._fixtures import BaseTestCase

from restaurants.models import Restaurant


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

    def test_admin(self):
        """Администратор видит информацию о ресторане"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_cheap_restaurant(info)


class RestaurantListTest(BaseTestCase):
    """
    Тесты для API получения списка всех ресторанов
    """

    def __get_url(self):
        return "/api/v1/restaurants/"

    def test_unauthorized(self):
        """Неавторизованный пользователь видит список ресторанов"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_some_user(self):
        """Зарегистрированный пользователь видит список ресторанов"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_cheap_worker(self):
        """Работник дешевого ресторана видит список ресторанов"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_cheap_owner(self):
        """Владелец дешевого ресторана видит список ресторанов"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_premium_worker(self):
        """Работник дорогого ресторана видит список ресторанов"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_premium_owner(self):
        """Владелец дорогого ресторана видит список ресторанов"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])

    def test_admin(self):
        """Администратор видит список ресторанов"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 2)
        self.verify_restaurant_list(info['results'])


class RestaurantCreateTest(BaseTestCase):
    """
    Тесты для API создания нового ресторана
    """

    def __get_url(self):
        return "/api/v1/restaurants/"

    def __post_new_restaurant_data(self):
        """
        Выполнить POST-запрос на добавление нового ресторана и вернуть ответ на
        него.
        """
        return self.client.post(
            self.__get_url(),
            {
                'translations': {
                    'en': {
                        'name': "New restaurant",
                        'description': "A new restaurant just added",
                    },
                    'ru': {
                        'name': "Новый ресторан",
                        'description': "Только что добавленный ресторан",
                    },
                },
                'country': 'Россия',
                'city': 'Москва',
                'street': 'Тверская',
                'building': '25',
                'address_details': 'Вход со двора',
                'zip_code': '110120',
                'longitude': '37.5',
                'latitude': '56.5'
            },
            format='json'
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может добавить ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        ans = self.__post_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был добавлен
        self.assertEqual(Restaurant.objects.count(), 2)

    def test_some_user(self):
        """Авторизованный пользователь добавляет новый ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        with self.logged_in('some_user'):
            ans = self.__post_new_restaurant_data()
        self.assertEqual(ans.status_code, 201)
        new_pk = ans.json()['id']
        # Проверяем, что ресторан был добавлен
        self.assertEqual(Restaurant.objects.count(), 3)
        new_restaurant = Restaurant.objects.get(pk=new_pk)
        self.assertEqual(new_restaurant.name, "New restaurant")
        self.assertEqual(new_restaurant.description, "A new restaurant just added")
        self.assertEqual(new_restaurant.city, "Москва")
        # Проверяем, что пользователь, добавивший ресторан, стал его владельцем
        self.assertTrue(
            new_restaurant.restaurant_staff.filter(
                position='owner', user=self._data['some_user']
            ).exists()
        )
        # Проверяем, что пользователь, добавивший ресторан, получил права владельца
        # этого ресторана
        self.assertTrue(new_restaurant.check_owner(self._data['some_user']))
        # Проверяем, что и русское название добавилось
        new_restaurant.set_current_language('ru')
        self.assertEqual(new_restaurant.name, "Новый ресторан")

    def test_cheap_worker(self):
        """Сотрудник дешевого ресторана добавляет новый ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        with self.logged_in('cheap_worker'):
            ans = self.__post_new_restaurant_data()
        self.assertEqual(ans.status_code, 201)
        new_pk = ans.json()['id']
        # Проверяем, что ресторан был добавлен
        self.assertEqual(Restaurant.objects.count(), 3)
        new_restaurant = Restaurant.objects.get(pk=new_pk)
        self.assertEqual(new_restaurant.name, "New restaurant")
        self.assertEqual(new_restaurant.description, "A new restaurant just added")
        self.assertEqual(new_restaurant.city, "Москва")
        # Проверяем, что пользователь, добавивший ресторан, стал его владельцем
        self.assertTrue(
            new_restaurant.restaurant_staff.filter(
                position='owner', user=self._data['cheap_worker']
            ).exists()
        )
        # Проверяем, что пользователь, добавивший ресторан, получил права владельца
        # этого ресторана
        self.assertTrue(new_restaurant.check_owner(self._data['cheap_worker']))
        # И остался сотрудником ресторана в котором работал раньше
        self.assertTrue(self._data['cheap_restaurant'].check_owner_or_worker(self._data['cheap_worker']))
        # И не получил новых прав по отношению к нему
        self.assertFalse(self._data['cheap_restaurant'].check_owner(self._data['cheap_worker']))
        # Проверяем, что и русское название добавилось
        new_restaurant.set_current_language('ru')
        self.assertEqual(new_restaurant.name, "Новый ресторан")

    def test_cheap_owner(self):
        """Владелец дешевого ресторана добавляет новый ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        with self.logged_in('cheap_owner'):
            ans = self.__post_new_restaurant_data()
        self.assertEqual(ans.status_code, 201)
        new_pk = ans.json()['id']
        # Проверяем, что ресторан был добавлен
        self.assertEqual(Restaurant.objects.count(), 3)
        new_restaurant = Restaurant.objects.get(pk=new_pk)
        self.assertEqual(new_restaurant.name, "New restaurant")
        self.assertEqual(new_restaurant.description, "A new restaurant just added")
        self.assertEqual(new_restaurant.city, "Москва")
        # Проверяем, что пользователь, добавивший ресторан, стал его владельцем
        self.assertTrue(
            new_restaurant.restaurant_staff.filter(
                position='owner', user=self._data['cheap_owner']
            ).exists()
        )
        # Проверяем, что пользователь, добавивший ресторан, получил права владельца
        # этого ресторана
        self.assertTrue(new_restaurant.check_owner(self._data['cheap_owner']))
        # И остался владельцем имевшегося у него ранее ресторана
        self.assertTrue(self._data['cheap_restaurant'].check_owner(self._data['cheap_owner']))
        # Проверяем, что и русское название добавилось
        new_restaurant.set_current_language('ru')
        self.assertEqual(new_restaurant.name, "Новый ресторан")

    def test_admin(self):
        """Администратор добавляет новый ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        with self.logged_in('admin'):
            ans = self.__post_new_restaurant_data()
        self.assertEqual(ans.status_code, 201)
        new_pk = ans.json()['id']
        # Проверяем, что ресторан был добавлен
        self.assertEqual(Restaurant.objects.count(), 3)
        new_restaurant = Restaurant.objects.get(pk=new_pk)
        self.assertEqual(new_restaurant.name, "New restaurant")
        self.assertEqual(new_restaurant.description, "A new restaurant just added")
        self.assertEqual(new_restaurant.city, "Москва")
        # Проверяем, что пользователь, добавивший ресторан, стал его владельцем
        self.assertTrue(
            new_restaurant.restaurant_staff.filter(
                position='owner', user=self._data['admin']
            ).exists()
        )
        # Проверяем, что пользователь, добавивший ресторан, получил права владельца
        # этого ресторана
        self.assertTrue(new_restaurant.check_owner(self._data['admin']))
        # Проверяем, что и русское название добавилось
        new_restaurant.set_current_language('ru')
        self.assertEqual(new_restaurant.name, "Новый ресторан")


class RestaurantUpdateTest(BaseTestCase):
    """
    Тесты для API изменения существующего ресторана
    """

    def __get_url(self, restaurant_name: str='cheap_restaurant'):
        return f"/api/v1/restaurants/{self._data[restaurant_name].pk}/"

    def __put_new_restaurant_data(self):
        """
        Выполнить PUT-запрос на изменение данных ресторана и вернуть ответ на
        него. Изменяет описание ресторана и его адрес
        """
        return self.client.put(
            self.__get_url(),
            {
                'translations': {
                    'en': {
                        'name': "A good place to eat",
                        'description': "Just some good place to eat",
                    },
                    'ru': {
                        'name': "Придорожное кафе",
                        'description': "Хорошее место чтобы перекусить",
                    },
                },
                'country': 'Россия',
                'city': 'Москва',
                'street': 'Ленинский проспект',
                'building': '8',
                'address_details': 'Второй этаж',
                'zip_code': '123456',
                'longitude': '37.5',
                'latitude': '56.5'
            },
            format='json'
        )

    def __verify_cheap_restaurant_changed(self):
        """
        Проверить, что данные о фастфуд-ресторане были успешно изменены
        """
        restaurant = Restaurant.objects.get(pk=self._data['cheap_restaurant'].pk)
        self.assertEqual(restaurant.name, "A good place to eat")
        self.assertEqual(restaurant.description, "Just some good place to eat")
        self.assertEqual(restaurant.country, "Россия")
        self.assertEqual(restaurant.city, "Москва")
        self.assertEqual(restaurant.street, "Ленинский проспект")
        self.assertEqual(restaurant.building, "8")
        self.assertEqual(restaurant.address_details, "Второй этаж")
        self.assertEqual(restaurant.zip_code, "123456")
        restaurant.set_current_language('ru')
        self.assertEqual(restaurant.name, "Придорожное кафе")
        self.assertEqual(restaurant.description, "Хорошее место чтобы перекусить")

    def test_unauthorized(self):
        """Неавторизованный пользователь не может редактировать информацию о ресторане"""
        ans = self.__put_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_some_user(self):
        """Пользователь не имеющий отношения к ресторану не может редактировать ресторан"""
        with self.logged_in('some_user'):
            ans = self.__put_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_cheap_worker(self):
        """Работник ресторана не может редактировать ресторан"""
        with self.logged_in('cheap_worker'):
            ans = self.__put_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_cheap_owner(self):
        """Владелец ресторана редактирует его описание и адрес"""
        with self.logged_in('cheap_owner'):
            ans = self.__put_new_restaurant_data()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что данные ресторана изменились
        self.__verify_cheap_restaurant_changed()

    def test_premium_worker(self):
        """Работник другого ресторана не может редактировать ресторан"""
        with self.logged_in('premium_worker'):
            ans = self.__put_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_premium_owner(self):
        """Владелец другого ресторана не может редактировать ресторан"""
        with self.logged_in('premium_owner'):
            ans = self.__put_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_admin(self):
        """Администратор редактирует описание и адрес ресторана"""
        with self.logged_in('admin'):
            ans = self.__put_new_restaurant_data()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что данные ресторана изменились
        self.__verify_cheap_restaurant_changed()


class RestaurantPatchTest(BaseTestCase):
    """
    Тесты для API частичного изменения существующего ресторана
    """

    def __get_url(self, restaurant_name: str='cheap_restaurant'):
        return f"/api/v1/restaurants/{self._data[restaurant_name].pk}/"

    def __patch_new_restaurant_data(self):
        """
        Выполнить PATCH-запрос на изменение данных ресторана и вернуть ответ на
        него. Изменяет подробности адреса ресторана
        """
        return self.client.patch(
            self.__get_url(),
            {
                'address_details': 'Вход со двора',
            },
            format='json'
        )

    def __verify_cheap_restaurant_changed(self):
        """
        Проверить, что данные о фастфуд-ресторане были успешно изменены
        """
        restaurant = Restaurant.objects.get(pk=self._data['cheap_restaurant'].pk)
        self.assertEqual(restaurant.name, "A good place to eat")
        self.assertEqual(restaurant.description, "Just some good place to eat")
        self.assertEqual(restaurant.country, "Russia")
        self.assertEqual(restaurant.city, "Moscow")
        self.assertEqual(restaurant.street, "Leninskiy avenue")
        self.assertEqual(restaurant.building, "6/3")
        self.assertEqual(restaurant.address_details, "Вход со двора")
        self.assertEqual(restaurant.zip_code, "123456")
        restaurant.set_current_language('ru')
        self.assertEqual(restaurant.name, "Придорожное кафе")
        self.assertEqual(restaurant.description, "Первое попавшееся кафе")

    def test_unauthorized(self):
        """Неавторизованный пользователь не может редактировать информацию о ресторане"""
        ans = self.__patch_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_some_user(self):
        """Пользователь не имеющий отношения к ресторану не может редактировать ресторан"""
        with self.logged_in('some_user'):
            ans = self.__patch_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_cheap_worker(self):
        """Работник ресторана не может редактировать ресторан"""
        with self.logged_in('cheap_worker'):
            ans = self.__patch_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_cheap_owner(self):
        """Владелец ресторана редактирует подробности его адреса"""
        with self.logged_in('cheap_owner'):
            ans = self.__patch_new_restaurant_data()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что данные ресторана изменились
        self.__verify_cheap_restaurant_changed()

    def test_premium_worker(self):
        """Работник другого ресторана не может редактировать ресторан"""
        with self.logged_in('premium_worker'):
            ans = self.__patch_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_premium_owner(self):
        """Владелец другого ресторана не может редактировать ресторан"""
        with self.logged_in('premium_owner'):
            ans = self.__patch_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_admin(self):
        """Администратор редактирует адрес ресторана"""
        with self.logged_in('admin'):
            ans = self.__patch_new_restaurant_data()
        self.assertEqual(ans.status_code, 200)
        # Проверяем, что данные ресторана изменились
        self.__verify_cheap_restaurant_changed()


class RestaurantDeleteTest(BaseTestCase):
    """
    Тесты для удаления существующего ресторана
    """

    def __get_url(self, restaurant_name: str='cheap_restaurant'):
        return f"/api/v1/restaurants/{self._data[restaurant_name].pk}/"

    def __delete_new_restaurant_data(self):
        """
        Выполнить DELETE-запрос на удаление ресторана и вернуть ответ на него
        """
        return self.client.delete(self.__get_url())

    def __verify_cheap_restaurant_deleted(self):
        """
        Проверить, что фастфуд-ресторан был удален
        """
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertFalse(
            Restaurant.objects.filter(pk=self._data['cheap_restaurant'].pk).exists()
        )

    def test_unauthorized(self):
        """Неавторизованный пользователь не может удалить ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        ans = self.__delete_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_some_user(self):
        """Зарегистрированный пользователь не может удалить ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        with self.logged_in('some_user'):
            ans = self.__delete_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()

    def test_cheap_worker(self):
        """Работник ресторана не может удалить ресторан"""
        self.assertEqual(Restaurant.objects.count(), 2)
        with self.logged_in('cheap_worker'):
            ans = self.__delete_new_restaurant_data()
        self.assertEqual(ans.status_code, 403)
        # Проверяем, что ресторан не был изменен
        self.verify_cheap_restaurant_unchanged()
