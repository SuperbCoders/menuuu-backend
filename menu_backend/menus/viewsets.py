"""
Наборы API-обработчиков для работы с меню, разделами меню и блюдами
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = (IsAuthenticated,)
    serializer_class = MenuCourseSerializer
    http_method_names = ['get', 'head', 'options']


class MenuSectionViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = MenuSection
    permission_classes = (IsAuthenticated,)
    serializer_class = MenuSectionSerializer
    http_method_names = ['get', 'head', 'options']


class MenuViewSet(viewsets.ModelViewSet):
    """
    Обработчики для работы с разделами меню
    """

    model = Menu
    permission_classes = (IsAuthenticated,)
    serializer_class = MenuSerializer
    http_method_names = ['get', 'head', 'options']
