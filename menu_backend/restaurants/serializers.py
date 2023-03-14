"""
Сериализаторы для данных ресторанов
"""

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from rest_framework.serializers import ModelSerializer, SlugField, ImageField

from restaurants.models import Restaurant, RestaurantCategory, RestaurantStaff

from menus.serializers import MenuSerializer


class RestaurantCategorySerializer(TranslatableModelSerializer):
    """Сериализатор для категорий ресторанов"""
    translations = TranslatedFieldsField(shared_model=RestaurantCategory)

    class Meta:
        model = RestaurantCategory
        fields = ['id', 'translations']


class RestaurantSerializer(TranslatableModelSerializer):
    """Сериализатор для ресторанов"""
    translations = TranslatedFieldsField(shared_model=Restaurant)
    # Нужно определить явно, чтобы сделать необязательным. Если
    # слаг не задан, то он будет id_{restaurant.pk}.
    slug = SlugField(required=False)
    logo = ImageField(required=False)
    picture = ImageField(required=False)

    class Meta:
        model = Restaurant
        fields = [
            'id',
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
            'twitter_profile',
            'facebook_profile',
            'instagram_profile',
            'average_receipt',
            # Только для чтения - подробная информация о категории ресторана и
            # текущем меню
            'category_data',
            'current_menu',
        ]

    category_data = RestaurantCategorySerializer(source='category', read_only=True)
    current_menu = MenuSerializer(read_only=True)


class RestaurantStaffSerializer(ModelSerializer):
    """Сериализатор для должностей пользователей в ресторанах"""
    class Meta:
        model = RestaurantStaff
        fields = [
            'restaurant',
            'user',
            'position'
        ]
