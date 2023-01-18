"""
Наборы API-обработчиков для работы с меню, разделами меню и блюдами
"""

from rest_framework import viewsets

from menus.models import MenuCourse, MenuSection, Menu
from menus.serializers import (
    MenuCourseSerializer,
    MenuSectionSerializer,
    MenuSerializer
)


class MenuCourseViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с блюдами
    """

    model = MenuCourse
    serializer_class = MenuCourseSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return MenuCourse.objects.all()


class MenuSectionViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = MenuSection
    serializer_class = MenuSectionSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return MenuSection.objects.all()


class MenuViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = Menu
    serializer_class = MenuSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return Menu.objects.filter(published=True)
