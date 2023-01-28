"""
Сериализаторы для чтения данных о тарифах
"""

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from rest_framework.serializers import ModelSerializer

from tariffs.models import Tariff


class TariffSerializer(TranslatableModelSerializer):
    """
    Сериализатор данных о тарифах
    """
    translations = TranslatedFieldsField(shared_model=Tariff)

    class Meta:
        model = Tariff
        fields = ['id', 'translations', 'month_price', 'year_price']
