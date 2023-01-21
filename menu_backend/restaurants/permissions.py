"""
Проверка прав доступа пользователей к ресторанам
"""

from rest_framework import permissions

from restaurants.models import RestaurantStaff


class RestaurantPermission(permissions.BasePermission):
    """
    Права доступа пользователей к ресторанам

    *   Любой пользователь, включая анонимного, имеет право получить информацию о
        ресторане или список всех ресторанов.

    *   Любой зарегистрированный пользователь имеет право добавить ресторан.

    *   Только владелец ресторана имеет право редактировать информацию о ресторане.

    *   Только владелец ресторана имеет право удалить ресторан.
    """

    def has_permission(self, request, view):
        """
        Проверка права на выполнения запроса request
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Проверка права на выполнения запроса request для ресторана obj
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if RestaurantStaff.objects.filter(user=request.user, restaurant=obj).exists():
            if RestaurantStaff.objects.get(user=request.user, restaurant=obj).position == 'owner':
                return True
        return False
