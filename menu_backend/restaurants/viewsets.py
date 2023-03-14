"""
Наборы обработчиков API для работы с ресторанами, категориями ресторанов и
должностями пользователей ресторанов.
"""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
    queryset = Restaurant.objects.all()
    permission_classes = [RestaurantPermission]
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
    http_method_names = ['get', 'head', 'options', 'post', 'put', 'patch', 'delete']

    def _check_slug(self, slug, instance=None):
        """
        Возвращает True, если указанное сокращенное название для URL может быть
        присвоено указанному ресторану. Значение True возвращается если значение
        slug пусто, либо совпадает с имеющимся слагом ресторана instance, либо
        не совпадает ни с одним слагом другого ресторана. Кроме того, проверяется,
        что если слаг имеет специальный формат id_XXX то XXX обязано совпадать
        с первичным ключом ресторана.
        """
        if not slug:
            return True
        if slug.lower.startswith("id_"):
            if instance and instance.pk and slug.lower() == f"id_{instance.pk}":
                return True
            return False
        if instance and slug.lower() == instance.slug.lower():
            return True
        if Restaurant.objects.filter(slug__iexact=slug).exists():
            return False
        return True

    def create(self, request):
        """
        При создании нового ресторана сделать пользователя, добавившего
        ресторан, в список владельцев этого ресторана
        """
        # Проверяем, что если никнейм ресторана задан, то он еще не принадлежит
        # другому ресторану
        slug = request.data.get('slug', None)
        if self.__check_slug(slug):
            return Response(
                {'detail': _("A restaurant with such slug string already exists")},
                status=400
            )
        response = super().create(request)
        if response.status_code == 201:
            # Находим созданный ресторан по возвращаемому значению ключа
            restaurant = Restaurant.objects.get(pk=response.data['id'])
            # И добавляем пользователя-создателя в список владельцев
            user = request.user
            if user.is_authenticated and user.is_active:
                restaurant.restaurant_staff.create(position='owner', user=user)
        return response

    def update(self, request, pk: int):
        """
        При изменении данных ресторана проверяем, что если изменен никнейм то он
        не используется другим рестораном
        """
        restaurant = get_object_or_404(Restaurant, pk=pk)
        # Проверяем, что если никнейм ресторана задан, то он еще не принадлежит
        # другому ресторану
        slug = request.data.get('slug', None)
        if self.__check_slug(slug, instance=restaurant):
            return Response(
                {'detail': _("A restaurant with such slug string already exists")},
                status=400
            )
        return super().update(request, pk=pk)

    def partial_update(self, request, pk: int):
        """
        При изменении данных ресторана проверяем, что если изменен никнейм то он
        не используется другим рестораном
        """
        restaurant = get_object_or_404(Restaurant, pk=pk)
        # Проверяем, что если никнейм ресторана задан, то он еще не принадлежит
        # другому ресторану
        slug = request.data.get('slug', None)
        if self.__check_slug(slug, instance=restaurant):
            return Response(
                {'detail': _("A restaurant with such slug string already exists")},
                status=400
            )
        return super().partial_update(request, pk=pk)

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

    @action(detail=False,
            methods=['get'],
            url_path='by_slug/(?P<slug>[A-Za-z0-9_-]+)/',
            permission_classes=[AllowAny],
            pagination_class=None)
    def by_slug(self, request, slug: str):
        """
        Получить информацию о ресторане по его никнейму
        """
        restaurant = get_object_or_404(Restaurant, slug__iexact=slug)
        return Response(RestaurantSerializer(restaurant).data)


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
