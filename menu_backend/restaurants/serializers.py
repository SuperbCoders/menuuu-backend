"""
Сериализаторы для данных ресторанов
"""

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from restaurants.models import Restaurant, RestaurantCategory

from menus.serializers import MenuSerializer


class RestaurantCategorySerializer(TranslatableModelSerializer):
    """Сериализатор для категорий ресторанов"""
    translations = TranslatedFieldsField(shared_model=RestaurantCategory)

    class Meta:
        model = RestaurantCategory
        fields = ['translations']


class RestaurantSerializer(TranslatableModelSerializer):
    """Сериализатор для ресторанов"""
    translations = TranslatedFieldsField(shared_model=Restaurant)

    class Meta:
        model = Restaurant
        fields = [
            'translations',
            'slug',
            'logo',
            'picture',
            'category',
            'stars',
            'country',
            'city',
            'street',
            'building',
            'address_details',
            'zip_code',
            'longitude',
            'latitude',
            'phone',
            'site',
            # Только для чтения - подробная информация о категории ресторана и
            # текущем меню
            'category_data',
            'current_menu',
        ]

    category_data = RestaurantCategorySerializer(source='category', read_only=True)
    current_menu = MenuSerializer(read_only=True)
