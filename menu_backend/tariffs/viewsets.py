"""
API для работы с тарифами
"""

from rest_framework import viewsets

from tariffs.models import Tariff
from tariffs.serializers import TariffSerializer
from tariffs.permissions import TariffPermission


class TariffViewSet(viewsets.ModelViewSet):
    model = Tariff
    permission_classes = [TariffPermission]
    serializer_class = TariffSerializer
    http_method_names = [
        'get', 'head', 'options', 'post', 'put', 'patch', 'delete'
    ]

    def get_queryset(self):
        return Tariff.objects.all()
