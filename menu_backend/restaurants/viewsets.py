"""
Наборы обработчиков API для работы с ресторанами, категориями ресторанов и
должностями пользователей ресторанов.
"""

from rest_framework import viewsets

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
    http_method_names = [
        'get', 'head', 'options', 'post', 'put', 'patch', 'delete'
    ]

    def get_queryset(self):
        return Restaurant.objects.all()

    def create(self, request):
        """
        При создании нового ресторана сделать пользователя, добавившего
        ресторан, в список владельцев этого ресторана
        """
        response = super().create(request)
        if response.status_code == 201:
            # Находим созданный ресторан по возвращаемому значению ключа
            restaurant = Restaurant.objects.get(pk=response.data['id'])
            # И добавляем пользователя-создателя в список владельцев
            user = request.user
            if user.is_authenticated and user.is_active:
                restaurant.restaurant_staff.create(position='owner', user=user)
        return response


class RestaurantStaffViewSet(viewsets.ModelViewSet):
    """
    Набор API-обработчиков для управления должностями пользователей
    в ресторанах
    """
    model = RestaurantStaff
    permission_classes = [RestaurantStaffPermission]
    serializer_class = RestaurantStaffSerializer
    http_method_names = [
        'get', 'head', 'options', 'post', 'put', 'patch', 'delete'
    ]

    def get_queryset(self):
        return RestaurantStaff.objects.all()
