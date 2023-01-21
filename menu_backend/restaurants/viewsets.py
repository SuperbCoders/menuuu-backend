from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from restaurants.models import Restaurant

from restaurants.serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    Набор API-обработчиков для управления ресторанами
    """
    model = Restaurant
    permission_classes = (AllowAny,)
    serializer_class = RestaurantSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return Restaurant.objects.all()
