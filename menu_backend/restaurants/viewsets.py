from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from restaurants.models import (
    Restaurant,
    RestaurantStaff,
    RestaurantCategory
)
from restaurants.permissions import (
    RestaurantPermission,
    RestaurantStaffPermission,
    RestaurantCategoryPermission
)
from restaurants.serializers import (
    RestaurantSerializer,
    RestaurantStaffSerializer,
    RestaurantCategorySerializer
)


class RestaurantCategoryViewSet(viewsets.ModelViewSet):
    """
    Набор API-обработчиков для управления категориями ресторанов.

    Смотреть категории ресторанов имеют право все пользователи, а изменять
    их - только администраторы.
    """
    model = RestaurantCategory
    permission_classes = [RestaurantCategoryPermission]
    serializer_class = RestaurantCategorySerializer
    http_method_names = [
        'get', 'head', 'options', 'post', 'put', 'patch', 'delete'
    ]

    def get_queryset(self):
        return RestaurantCategory.objects.all()


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    Набор API-обработчиков для управления ресторанами
    """
    model = Restaurant
    permission_classes = [RestaurantPermission]
    serializer_class = RestaurantSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return Restaurant.objects.all()


class RestaurantStaffViewSet(viewsets.ModelViewSet):
    """
    Набор API-обработчиков для управления должностями пользователей
    в ресторанах
    """
    model = RestaurantStaff
    permission_classes = [RestaurantStaffPermission]
    serializer_class = RestaurantStaffSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return RestaurantStaff.objects.all()
