"""
Проверка прав доступа пользователей к ресторанам
"""

from rest_framework import permissions

from restaurants.models import Restaurant


class RestaurantCategoryPermission(permissions.BasePermission):
    """
    С правами доступа к категориям ресторанов все просто. Все пользователи могут
    видеть все категории, а изменять их имеет право только администратора.
    """

    def has_permission(self, request, view):
        """
        Проверка права на выполнения запроса request
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated or not request.user.is_active:
            return False
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """
        Проверка права на выполнения запроса request для ресторана obj
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated or not request.user.is_active:
            return False
        return request.user.is_staff


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
        if not request.user.is_authenticated or not request.user.is_active:
            return False
        if request.method == 'POST':
            return True
        # Редактировать ресторан может администратор или владелец ресторана
        # Более подробная проверка делается в has_object_permission
        return request.user.is_staff or request.user.restaurant_staff.exists()

    def has_object_permission(self, request, view, obj):
        """
        Проверка права на выполнения запроса request для ресторана obj
        """
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
        return obj.check_owner(request.user)


class RestaurantStaffPermission(permissions.BasePermission):
    """
    Права доступа пользователей к ресторанам

    *   Владелец или сотрудник ресторана имеет право видеть информацию о том
        кто еще работает в этом ресторане

    *   Только владелец ресторана имеет право изменять должности пользователей
        в ресторане, добавлять и удалять его работников.
    """

    def has_permission(self, request, view):
        """
        Проверка права на выполнения запроса request
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and request.user.is_active
        if request.method == 'POST':
            # При добавлении нового сотрудника придется извлекать идентификатор
            # ресторана из данных запроса и проверять права для него...
            restaurant_id = request.DATA['restaurant']
            if not Restaurant.objects.filter(pk=restaurant_id).exists():
                return False
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            return restaurant.check_owner(request.user)
        return request.user.is_staff or request.user.restaurant_staff.exists()

    def has_object_permission(self, request, view, obj):
        """
        Проверка права на выполнения запроса request для ресторана obj
        """
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.restaurant.check_owner_or_worker(request.user)
        return obj.restaurant.check_owner(request.user)
