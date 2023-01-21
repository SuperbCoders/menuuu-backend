from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from restaurants.models import Restaurant
from restaurants.swagger import swagger_public_menu


def course_to_json(course, language: str = settings.LANGUAGE_CODE):
    """
    Возвращает dict-oбъект с информацией о блюде
    """
    course.set_current_language(language)
    return {
        'title': course.title,
        'composition': course.composition,
        'price': course.price,
        'cooking_time': course.cooking_time
    }


def section_to_json(section, language: str = settings.LANGUAGE_CODE):
    """
    Возвращает dict-oбъект с информацией о разделе меню, включающей заголовок раздела
    и описание блюд
    """
    section.set_current_language(language)
    obj = {'title': section.title, 'courses': []}
    for course in section.courses.filter(published=True).all():
        obj['courses'].append(course_to_json(course, language))
    return obj


def menu_to_json(menu, language: str = settings.LANGUAGE_CODE):
    """
    Возвращает dict-объект с информацией о меню для пользователя.

    Возвращается объект хранящий три поля - 'title', 'sections' и 'courses'.
    Здесь 'title' - это строка заголовка меню. Значения двух других полей
    являются списками и могут быть (но не одновременно) пустыми. В списке
    'sections' будет информация о раделах меню, например, 'супы', 'закуски',
    'десерты', 'напитки' и. т.п. В списке 'courses' будут отдельные блюда, не
    вошедшие ни в один раздел меню.
    """
    menu.set_current_language(language)
    obj = {'sections': [], 'courses': [], 'title': menu.title}
    for section in menu.sections.all():
        obj['sections'].append(section_to_json(section, language))
    for course in menu.courses.filter(section__isnull=True, published=True).all():
        obj['courses'].append(course_to_json(course, language))
    return obj;


def restaurant_to_json(restaurant, language: str = settings.LANGUAGE_CODE):
    """
    Возвращает dict-объект с информацией о ресторане и его текущем меню.

    Параметры
    ---------
    restaurant: Restaurant
        Объект ресторана, меню которого запросил пользователь

    language: str
        Язык, на который следует перевести меню, по умолчанию используется язык,
        установленный по умолчанию для приложения.
    """
    restaurant.set_current_language(language)
    obj = {
        'id': restaurant.pk,
        'name': restaurant.name,
        'description': restaurant.description,
        'phone': str(restaurant.phone),
        'site': restaurant.site
    }
    if restaurant.logo:
        obj['logo'] = restaurant.logo.url
    if restaurant.picture:
        obj['picture'] = restaurant.picture.url
    if restaurant.category:
        restaurant.category.set_current_language(language)
        obj['category'] = {
            'name': restaurant.category.name,
        }
    obj['stars'] = restaurant.stars
    obj['address'] = {
        'country': restaurant.country,
        'city': restaurant.city,
        'street': restaurant.street,
        'building': restaurant.building,
        'address_details': restaurant.address_details,
        'zip_code': restaurant.zip_code,
        'latitude': restaurant.latitude,
        'longitude': restaurant.longitude
    }
    menu = restaurant.current_menu
    if menu:
        obj['menu'] = menu_to_json(menu, language)
    return obj


class UnauthorizedRestaturantView(APIView):
    """
    Просмотр неавторизованным пользователем информации о ресторане. Поддерживает
    только метод GET, который возвращает информацию о ресторане и меню этого ресторана.
    """

    def __get_language(self, request):
        """
        Получить язык из параметров GET-запроса
        """
        language = request.GET.get('language', settings.LANGUAGE_CODE)
        if not isinstance(language, str):
            language = language[0]
        return language

    @swagger_public_menu
    def get(self, request, pk: int):
        """Возврат информации о меню ресторана"""
        language = self.__get_language(request)
        restaurant = get_object_or_404(Restaurant, pk=pk)
        data = restaurant_to_json(restaurant, language)
        return Response(data, status=200)
