"""
Наборы API-обработчиков для работы с меню, разделами меню и блюдами
"""

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

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
    queryset = MenuCourse.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MenuCourseSerializer
    http_method_names = ['get', 'head', 'options']


class MenuSectionViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = MenuSection
    queryset = MenuSection.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = MenuSectionSerializer
    http_method_names = ['get', 'head', 'options']


class MenuViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = Menu
    permission_classes = (AllowAny,)
    serializer_class = MenuSerializer
    http_method_names = ['get', 'head', 'options']

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
