"""
Тесты для API для работы с блюдами
"""

import datetime

from menus.models import MenuCourse
from restaurants.tests._fixtures import BaseTestCase


class MenuCourseListTest(BaseTestCase):
    """
    Тесты для API получения списка блюд
    """

    def __get_url(self):
        return '/api/v1/menu_courses/'

    def test_unauthorized(self):
        """Неавторизованный пользователь просматривает список всех опубликованных блюд"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_some_user(self):
        """Пользователь без разрешений просматривает список всех опубликованных блюд"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_cheap_worker(self):
        """Сотрудник первого ресторана видит все бдюда включая неопубликованные"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 4)
        self.assertEqual(len(info['results']), 4)

    def test_cheap_owner(self):
        """Хозяин первого ресторана видит все бдюда включая неопубликованные"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 4)
        self.assertEqual(len(info['results']), 4)

    def test_premium_worker(self):
        """Работник ресторана не видит неопубликованных блюд другого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_premium_owner(self):
        """Хозяин ресторана не видит неопубликованных блюд другого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 3)
        self.assertEqual(len(info['results']), 3)

    def test_admin(self):
        """Администратор видит все бдюда включая неопубликованные"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        info = ans.json()
        self.assertEqual(info['count'], 4)
        self.assertEqual(len(info['results']), 4)


class PublishedMenuCourseRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об определенном опубликованном блюде
    """

    def __get_url(self):
        return f"/api/v1/menu_courses/{self._data['chocolate_sandwich'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь может видеть опубликованное блюдо"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())

    def test_some_user(self):
        """Зарегистрированный пользователь может видеть опубликованное блюдо"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())

    def test_cheap_worker(self):
        """Работник ресторана может видеть опубликованное блюдо своего ресторана"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())

    def test_cheap_owner(self):
        """Хозяин ресторана может видеть опубликованное блюдо своего ресторана"""
        with self.logged_in('cheap_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())

    def test_premium_worker(self):
        """Работник ресторана может видеть опубликованное блюдо чужого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())

    def test_premium_owner(self):
        """Хозяин ресторана может видеть опубликованное блюдо чужого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())

    def test_admin(self):
        """Администратор может видеть опубликованное блюдо"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_chocolate_sandwich(ans.json())


class UnpublishedMenuCourseRetrieveTest(BaseTestCase):
    """
    Тесты для API получения информации об определенном неопубликованном блюде
    """

    def __get_url(self):
        return f"/api/v1/menu_courses/{self._data['disabled_water'].pk}/"

    def test_unauthorized(self):
        """Неавторизованный пользователь не видит неопубликованное блюдо"""
        ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_some_user(self):
        """Зарегистрированный пользователь не видит неопубликованное блюдо"""
        with self.logged_in('some_user'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_cheap_worker(self):
        """Работник ресторана видит неопубликованное блюдо своего ресторана"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_disabled_water(ans.json())

    def test_cheap_owner(self):
        """Хозяин ресторана видит неопубликованное блюдо своего ресторана"""
        with self.logged_in('cheap_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_disabled_water(ans.json())

    def test_premium_worker(self):
        """Работник ресторана не видит неопубликованное блюдо чужого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_premium_owner(self):
        """Хозяин ресторана не видит неопубликованное блюдо чужого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 404)

    def test_admin(self):
        """Администратор видит любое неопубликованное блюдо"""
        with self.logged_in('admin'):
            ans = self.client.get(self.__get_url())
        self.assertEqual(ans.status_code, 200)
        self.verify_disabled_water(ans.json())


class MenuCourseCreateTest(BaseTestCase):
    """
    Тесты для API создания нового блюда
    """

    def __get_url(self):
        return '/api/v1/menu_courses/'

    def __post_new_course_data(self):
        """Выполнить POST-запрос для создания нового блюда и вернуть результат"""
        return self.client.post(
            self.__get_url(),
            {
                'translations': {
                    'en': {'title': "Pie with jam"},
                    'ru': {'title': "Пирожок с вареньем"},
                },
                'menu': self._data['cheap_menu'].pk,
                'section': self._data['desserts_section'].pk,
                'published': True,
                'price': 45,
                'cooking_time': datetime.timedelta(seconds=150)
            },
            format='json'
        )

    def __verify_new_course(self, pk):
        """
        Проверить, что новое блюдо добавилось в базу по первичному ключу pk
        """
        self.assertEqual(MenuCourse.objects.count(), 5)
        course = MenuCourse.objects.get(pk=pk)
        self.assertEqual(course.menu, self._data['cheap_menu'])
        self.assertEqual(course.section, self._data['desserts_section'])
        self.assertEqual(course.published, True)
        self.assertEqual(course.price, 45)
        self.assertEqual(course.cooking_time.total_seconds(), 150)
        self.assertEqual(course.title, "Pie with jam")
        course.set_current_language('ru')
        self.assertEqual(course.title, "Пирожок с вареньем")

    def __verify_no_new_course(self):
        """Проверить, что никакого нового блюда не было добавлено"""
        self.assertEqual(MenuCourse.objects.count(), 4)

    def test_unauthorized(self):
        """Неавторизованный пользователь не может добавить блюдо"""
        self.__verify_no_new_course()
        ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 401)
        self.__verify_no_new_course()

    def test_some_user(self):
        """Пользователь не работающий в ресторане не может добавить блюдо"""
        self.__verify_no_new_course()
        with self.logged_in('some_user'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_cheap_worker(self):
        """Работник ресторана может добавить блюдо в меню этого ресторана"""
        self.__verify_no_new_course()
        with self.logged_in('cheap_worker'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 201)
        self.__verify_new_course(ans.json()['id'])

    def test_cheap_owner(self):
        """Хозяин ресторана может добавить блюдо в меню этого ресторана"""
        self.__verify_no_new_course()
        with self.logged_in('cheap_owner'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 201)
        self.__verify_new_course(ans.json()['id'])

    def test_premium_worker(self):
        """Работник ресторана не может добавить блюдо в меню другого ресторана"""
        self.__verify_no_new_course()
        with self.logged_in('premium_worker'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_premium_owner(self):
        """Хозяин ресторана не может добавить блюдо в меню другого ресторана"""
        self.__verify_no_new_course()
        with self.logged_in('premium_owner'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_admin(self):
        """Администратор добавляет блюдо в меню ресторана"""
        self.__verify_no_new_course()
        with self.logged_in('admin'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 201)
        self.__verify_new_course(ans.json()['id'])


class MenuCourseCreateInvalidTest(BaseTestCase):
    """
    Тесты для API создания нового блюда - проверяют, что нельзя создать блюдо,
    не привязанное к конкретному меню.

    Поскольку производится проверка прав доступа пользователя к меню, в случае
    отсутствия идентификатора меню возвращается ошибка 403 а не 400.
    """

    def __get_url(self):
        return '/api/v1/menu_courses/'

    def __post_new_course_data(self):
        """Выполнить POST-запрос для создания нового блюда и вернуть результат"""
        return self.client.post(
            self.__get_url(),
            {
                'translations': {
                    'en': {'title': "Pie with jam"},
                    'ru': {'title': "Пирожок с вареньем"},
                },
                'section': self._data['desserts_section'].pk,
                'published': True,
                'price': 45,
                'cooking_time': datetime.timedelta(seconds=150)
            },
            format='json'
        )

    def __verify_no_new_course(self):
        """Проверить, что никакого нового блюда не было добавлено"""
        self.assertEqual(MenuCourse.objects.count(), 4)

    def test_unauthorized(self):
        """Неавторизованный пользователь не может добавить блюдо"""
        self.__verify_no_new_course()
        ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 401)
        self.__verify_no_new_course()

    def test_some_user(self):
        """Пользователь не работающий в ресторане не может добавить блюдо"""
        self.__verify_no_new_course()
        with self.logged_in('some_user'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_cheap_worker(self):
        """Работник первого ресторана не может добавить блюдо не указав меню"""
        self.__verify_no_new_course()
        with self.logged_in('cheap_worker'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_cheap_owner(self):
        """Хозяин первого ресторана не может добавить блюдо не указав меню"""
        self.__verify_no_new_course()
        with self.logged_in('cheap_owner'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_premium_worker(self):
        """Работник второго ресторана не может добавить блюдо не указав меню"""
        self.__verify_no_new_course()
        with self.logged_in('premium_worker'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_premium_owner(self):
        """Хозяин второго ресторана не может добавить блюдо не указав меню"""
        self.__verify_no_new_course()
        with self.logged_in('premium_owner'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()

    def test_admin(self):
        """АДминистратор не может добавить блюдо не указав меню"""
        self.__verify_no_new_course()
        with self.logged_in('admin'):
            ans = self.__post_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_no_new_course()


class PublishedMenuCourseUpdateTest(BaseTestCase):
    """
    Тесты для API обновления информации об определенном опубликованном блюде
    """

    def __get_url(self):
        return f"/api/v1/menu_courses/{self._data['chocolate_sandwich'].pk}/"

    def __put_new_course_data(self):
        """Послать PUT-запрос на обновление данных о блюде и вернуть ответ"""
        return self.client.put(
            self.__get_url(),
            {
                'translations': {
                    'en': {'title': "Sandwich with chocolate butter"},
                    'ru': {'title': "Бутерброд с шоколадным маслом"},
                },
                'menu': self._data['cheap_menu'].pk,
                'section': self._data['desserts_section'].pk,
                'published': True,
                'price': 40,  # Было 30
                'cooking_time': datetime.timedelta(seconds=60)  # Было 90
            },
            format='json'
        )

    def __verify_course_unchanged(self):
        """Проверить, что информация о блюде не изменилась"""
        course = MenuCourse.objects.get(pk=self._data['chocolate_sandwich'].pk)
        self.assertEqual(course.menu.pk, self._data['cheap_menu'].pk)
        self.assertEqual(course.section.pk, self._data['desserts_section'].pk)
        self.assertEqual(course.price, 30)
        self.assertEqual(course.cooking_time.total_seconds(), 90)
        self.assertEqual(course.title, "Sandwich with chocolate butter")
        course.set_current_language('ru')
        self.assertEqual(course.title, "Бутерброд с шоколадным маслом")

    def __verify_course_changed(self):
        """Проверить, что информация о блюде изменилась как надо"""
        course = MenuCourse.objects.get(pk=self._data['chocolate_sandwich'].pk)
        self.assertEqual(course.menu.pk, self._data['cheap_menu'].pk)
        self.assertEqual(course.section.pk, self._data['desserts_section'].pk)
        self.assertEqual(course.price, 40)
        self.assertEqual(course.cooking_time.total_seconds(), 60)
        self.assertEqual(course.title, "Sandwich with chocolate butter")
        course.set_current_language('ru')
        self.assertEqual(course.title, "Бутерброд с шоколадным маслом")

    def test_unauthorized(self):
        """Неавторизованный пользователь не может изменить блюдо"""
        ans = self.__put_new_course_data()
        self.assertEqual(ans.status_code, 401)
        self.__verify_course_unchanged()

    def test_some_user(self):
        """Пользователь не связанный с рестораном не может изменить блюдо"""
        with self.logged_in('some_user'):
            ans = self.__put_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_course_unchanged()

    def test_cheap_worker(self):
        """Работник ресторана изменяет информацию о блюде"""
        with self.logged_in('cheap_worker'):
            ans = self.__put_new_course_data()
        self.assertEqual(ans.status_code, 200)
        self.__verify_course_changed()

    def test_cheap_owner(self):
        """Хозяин ресторана изменяет информацию о блюде"""
        with self.logged_in('cheap_owner'):
            ans = self.__put_new_course_data()
        self.assertEqual(ans.status_code, 200)
        self.__verify_course_changed()

    def test_premium_worker(self):
        """Работник ресторана не может изменить блюдо другого ресторана"""
        with self.logged_in('premium_worker'):
            ans = self.__put_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_course_unchanged()

    def test_premium_owner(self):
        """Хозяин ресторана не может изменить блюдо другого ресторана"""
        with self.logged_in('premium_owner'):
            ans = self.__put_new_course_data()
        self.assertEqual(ans.status_code, 403)
        self.__verify_course_unchanged()

    def test_admin(self):
        """Администратор изменяет информацию о блюде"""
        with self.logged_in('admin'):
            ans = self.__put_new_course_data()
        self.assertEqual(ans.status_code, 200)
        self.__verify_course_changed()
