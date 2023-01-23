from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from restaurants.models import Restaurant, RestaurantStaff, RestaurantCategory
from restaurants.permissions import RestaurantPermission, RestaurantStaffPermission, RestaurantCategoryPermission
from restaurants.serializers import RestaurantSerializer, RestaurantStaffSerializer, RestaurantCategorySerializer


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


class RestaurantStaffViewset(viewsets.ModelViewSet):
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
