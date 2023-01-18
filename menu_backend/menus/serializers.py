"""
Сериализация данных о меню, разделах меню и блюдах
"""

from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField

from menus.models import Menu, MenuSection, MenuCourse


class MenuCourseSerializer(TranslatableModelSerializer):
    """Сериализатор для блюд"""
    translations = TranslatedFieldsField(shared_model=MenuCourse)

    class Meta:
        model = MenuCourse
        fields = ['id', 'translations', 'price', 'cooking_time']


class MenuSectionSerializer(TranslatableModelSerializer):
    """Сериализатор для разделов меню"""
    translations = TranslatedFieldsField(shared_model=MenuCourse)

    class Meta:
        model = MenuCourse
        fields = ['translations', 'courses']

    # Вместе с разделом меню возвращаем информацию обо всех блюда этого
    # раздела
    courses = MenuCourseSerializer(many=True, read_only=True)


class MenuSerializer(TranslatableModelSerializer):
    """Сериализатор для меню"""
    translations = TranslatedFieldsField(shared_model=Menu)

    class Meta:
        model = Menu
        fields = ['translations', 'sections', 'restaurant']

    # При возврате меню расписать все его разделы и блюда
    sections = MenuSectionSerializer(many=True, read_only=True)
