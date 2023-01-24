"""
Наборы API-обработчиков для работы с меню, разделами меню и блюдами
"""

from django.db.models import Q

from rest_framework import viewsets

from menus.models import MenuCourse, MenuSection, Menu
from menus.permissions import (
    MenuPermission,
    MenuSectionPermission,
    MenuCoursePermission
)
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
    queryset = MenuCourse.objects.all()
    permission_classes = [MenuCoursePermission]
    serializer_class = MenuCourseSerializer
    http_method_names = ['get', 'head', 'options', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        """
        Возвращает список блюд, которые может видеть текущий пользователь.

        Неавторизованный пользователь может видеть только блюда опубликованных
        меню. Авторизованный пользователь может видеть блюда опубликованных меню
        и блюда меню своих ресторанов.
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return MenuSection.objects.all()
            return MenuSection.objects.filter(
                Q(menu__published=True) |
                Q(menu__restaurant__id__in=self.request.user.restaurant_staff.values_list('restaurant_id', flat=True))
            ).all()
        return MenuSection.objects.filter(menu__published=True).all()


class MenuSectionViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = MenuSection
    queryset = MenuSection.objects.all()
    permission_classes = [MenuSectionPermission]
    serializer_class = MenuSectionSerializer
    http_method_names = ['get', 'head', 'options', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        """
        Возвращает список разделов меню, которые может видеть текущий пользователь.

        Неавторизованный пользователь может видеть только разделы опубликованных
        меню. Авторизованный пользователь может видеть разделы опубликованных меню
        и разделы меню своих ресторанов.
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return MenuSection.objects.all()
            return MenuSection.objects.filter(
                Q(menu__published=True) |
                Q(menu__restaurant__id__in=self.request.user.restaurant_staff.values_list('restaurant_id', flat=True))
            ).all()
        return MenuSection.objects.filter(menu__published=True).all()


class MenuViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = Menu
    permission_classes = [MenuPermission]
    serializer_class = MenuSerializer
    http_method_names = ['get', 'head', 'options', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        """
        Возвращает список меню, которые может видеть текущий пользователь.

        Неавторизованный пользователь может видеть только опубликованные меню.
        Авторизованный пользователь может видеть опубликованные меню и меню своих
        ресторанов
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return Menu.objects.all()
            return Menu.objects.filter(
                Q(published=True) |
                Q(restaurant__id__in=self.request.user.restaurant_staff.values_list('restaurant_id', flat=True))
            ).all()
        return Menu.objects.filter(published=True).all()
