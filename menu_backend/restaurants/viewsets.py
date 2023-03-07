"""
Наборы обработчиков API для работы с ресторанами, категориями ресторанов и
должностями пользователей ресторанов.
"""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.decorators import action
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
from restaurants.swagger import swagger_qrcode


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

    @swagger_qrcode
    @action(detail=True, methods=['get'], url_path='qrcode', permission_classes=[AllowAny])
    def qrcode(self, request, pk: int):
        """
        Вернуть изображение qr-кода для заданного ресторана
        """
        restaurant = get_object_or_404(Restaurant, pk=pk)
        response = HttpResponse(content_type='image/png')
        restaurant.generate_qrcode().save(response, "PNG")
        response['Content-Disposition'] = 'attachment; filename="qrcode.png"'
        return response


class RestaurantStaffViewSet(viewsets.ModelViewSet):
    """
    Набор API-обработчиков для управления должностями пользователей
    в ресторанах
    """
    model = RestaurantStaff
    queryset = RestaurantStaff.objects.all()
    permission_classes = [RestaurantStaffPermission]
    serializer_class = RestaurantStaffSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restaurant', 'user']
    http_method_names = ['get', 'head', 'options', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        """
        Список сотрудников ресторанов видимых пользователю request.user
        """
        if not self.request.user.is_authenticated:
            return RestaurantStaff.objects.filter(id__in=set())
        if self.request.user.is_staff:
            return RestaurantStaff.objects.all()
        restaurant_ids = set(
            self.request.user.restaurant_staff.values_list('restaurant_id', flat=True)
        )
        return RestaurantStaff.objects.filter(restaurant__id__in=restaurant_ids)
