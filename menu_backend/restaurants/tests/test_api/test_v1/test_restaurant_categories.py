"""
Тесты для стандартных REST API для работы с ресторанами
"""

from restaurants.tests._fixtures import BaseTestCase

from restaurants.models import RestaurantCategory


class RestaurantCategoryRetrieveTest(BaseTestCase):
    """
    Тесты для API для получения информации о категории ресторанов.
    """

    def __get_url(self):
        return f"/api/v1/restaurant_categories/{self._data['category'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь видит информацию о категории ресторанов"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_fastfood_category(info)

    def test_some_user(self):
        """Непривилегированный пользователь видит информацию о категории ресторанов"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_fastfood_category(info)

    def test_cheap_worker(self):
        """Работник дешевого ресторана пользователь видит информацию о категории ресторанов"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_fastfood_category(info)

    def test_cheap_owner(self):
        """Владелец дешевого ресторана пользователь видит информацию о категории ресторанов"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_fastfood_category(info)

    def test_premium_worker(self):
        """Работник дорогого ресторана пользователь видит информацию о категории ресторанов"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_fastfood_category(info)

    def test_premium_owner(self):
        """Владелец дорогого ресторана пользователь видит информацию о категории ресторанов"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_fastfood_category(info)

    def test_admin(self):
        """Администратор видит информацию о категории ресторанов"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.verify_fastfood_category(info)


class RestaurantCategoryListTest(BaseTestCase):
    """
    Тесты для API для получения списка категорий ресторанов.
    """

    def __get_url(self):
        return "/api/v1/restaurant_categories/"

    def test_unauthorized(self):
        """Неавторизованный пользователь видит список категорий ресторанов"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertIsInstance(info['results'], list)
        self.assertEqual(len(info['results']), 1)
        self.verify_fastfood_category(info['results'][0])

    def test_some_user(self):
        """Непривилегированный пользователь видит список категорий ресторанов"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertIsInstance(info['results'], list)
        self.assertEqual(len(info['results']), 1)
        self.verify_fastfood_category(info['results'][0])

    def test_cheap_worker(self):
        """Работник дешевого ресторана пользователь видит список категорий ресторанов"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertIsInstance(info['results'], list)
        self.assertEqual(len(info['results']), 1)
        self.verify_fastfood_category(info['results'][0])

    def test_cheap_owner(self):
        """Владелец дешевого ресторана пользователь видит список категорий ресторанов"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertIsInstance(info['results'], list)
        self.assertEqual(len(info['results']), 1)
        self.verify_fastfood_category(info['results'][0])

    def test_premium_worker(self):
        """Работник дорогого ресторана пользователь видит список категорий ресторанов"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertIsInstance(info['results'], list)
        self.assertEqual(len(info['results']), 1)
        self.verify_fastfood_category(info['results'][0])

    def test_premium_owner(self):
        """Владелец дорогого ресторана пользователь видит список категорий ресторанов"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertIsInstance(info['results'], list)
        self.assertEqual(len(info['results']), 1)
        self.verify_fastfood_category(info['results'][0])

    def test_admin(self):
        """Администратор видит список категорий ресторанов"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertIsInstance(info['results'], list)
        self.assertEqual(len(info['results']), 1)
        self.verify_fastfood_category(info['results'][0])


class RestaurantCategoryCreateTest(BaseTestCase):
    """
    Тесты для API для добавления новой категории ресторанов.
    """

    def __get_url(self):
        return "/api/v1/restaurant_categories/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не может добавить категорию ресторанов"""
        self.assertEqual(RestaurantCategory.objects.count(), 1)
        ans = self.client.post(
            self.__get_url(),
            {
                'translations': {'en': {'name': "Vegetarian"}}
            },
            format='json'
        )
        self.assertEqual(ans.status_code, 403)
        # Проверить, что категория не была добавлена
        self.assertEqual(RestaurantCategory.objects.count(), 1)

    def test_some_user(self):
        """Непривилегированный пользователь не может добавить категорию ресторанов"""
        self.assertEqual(RestaurantCategory.objects.count(), 1)
        with self.logged_in('some_user'):
            ans = self.client.post(
                self.__get_url(),
                {
                    'translations': {'en': {'name': "Vegetarian"}}
                },
                format='json'
            )
        self.assertEqual(ans.status_code, 403)
        # Проверить, что категория не была добавлена
        self.assertEqual(RestaurantCategory.objects.count(), 1)

    def test_cheap_worker(self):
        """Работник дешевого ресторана не может добавить категорию ресторанов"""
        self.assertEqual(RestaurantCategory.objects.count(), 1)
        with self.logged_in('cheap_worker'):
            ans = self.client.post(
                self.__get_url(),
                {
                    'translations': {'en': {'name': "Vegetarian"}}
                },
                format='json'
            )
        self.assertEqual(ans.status_code, 403)
        # Проверить, что категория не была добавлена
        self.assertEqual(RestaurantCategory.objects.count(), 1)

    def test_cheap_owner(self):
        """Владелец дешевого ресторана не может добавить категорию ресторанов"""
        self.assertEqual(RestaurantCategory.objects.count(), 1)
        with self.logged_in('cheap_owner'):
            ans = self.client.post(
                self.__get_url(),
                {
                    'translations': {'en': {'name': "Vegetarian"}}
                },
                format='json'
            )
        self.assertEqual(ans.status_code, 403)
        # Проверить, что категория не была добавлена
        self.assertEqual(RestaurantCategory.objects.count(), 1)

    def test_premium_worker(self):
        """Работник премиум ресторана не может добавить категорию ресторанов"""
        self.assertEqual(RestaurantCategory.objects.count(), 1)
        with self.logged_in('premium_worker'):
            ans = self.client.post(
                self.__get_url(),
                {
                    'translations': {'en': {'name': "Vegetarian"}}
                },
                format='json'
            )
        self.assertEqual(ans.status_code, 403)
        # Проверить, что категория не была добавлена
        self.assertEqual(RestaurantCategory.objects.count(), 1)

    def test_premium_owner(self):
        """Владелец премиум ресторана не может добавить категорию ресторанов"""
        self.assertEqual(RestaurantCategory.objects.count(), 1)
        with self.logged_in('premium_owner'):
            ans = self.client.post(
                self.__get_url(),
                {
                    'translations': {'en': {'name': "Vegetarian"}}
                },
                format='json'
            )
        self.assertEqual(ans.status_code, 403)
        # Проверить, что категория не была добавлена
        self.assertEqual(RestaurantCategory.objects.count(), 1)

    def test_admin(self):
        """Администратор добавляет новую категорию ресторанов"""
        self.assertEqual(RestaurantCategory.objects.count(), 1)
        with self.logged_in('admin'):
            ans = self.client.post(
                self.__get_url(),
                {
                    'translations': {'en': {'name': "Vegetarian"}}
                },
                format='json'
            )
        self.assertEqual(ans.status_code, 201)
        self.assertEqual(ans.json()['translations']['en']['name'], "Vegetarian")
        new_pk = ans.json()['id']
        # Проверить, что категория была добавлена
        self.assertEqual(RestaurantCategory.objects.count(), 2)
        self.assertEqual(RestaurantCategory.objects.get(pk=new_pk).name, "Vegetarian")
