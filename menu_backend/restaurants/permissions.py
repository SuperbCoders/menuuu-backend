"""
Проверка прав доступа пользователей к ресторанам
"""

from rest_framework import permissions

from restaurants.models import RestaurantStaff, Restaurant


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
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """
        Проверка права на выполнения запроса request для ресторана obj
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
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
        if not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Проверка права на выполнения запроса request для ресторана obj
        """
        if request.method in permissions.SAFE_METHODS:
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
        # Либо просмотр списка, либо добавление нового сотрудника к ресторану.
        if request.method in permissions.SAFE_METHODS:
            # В первом случае разрешаем просмотр всем зарегистрированным пользователем,
            # а переопределенная функция get_queryset наборе обработчиков ограничит
            # список доступных должностей пользователей в ресторанами теми ресторанами,
            # к которым пользователь имеет доступ.
            return request.user.is_authenticated:
        if request.method == 'POST':
            # А вот во втором случае придется извлекать идентификатор ресторана из
            # данных запроса и проверять права для него...
            restaurant_id = request.DATA['restaurant']
            print(f"Restaurant ID is {restaurant_id}")
            if not Restaurant.objects.filter(pk=restaurant_id).exists():
                return False
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            return restaurant.check_owner(request.user)
        return False

    def has_object_permission(self, request, view, obj):
        """
        Проверка права на выполнения запроса request для ресторана obj
        """
        if request.method in permissions.SAFE_METHODS:
            return obj.restaurant.check_owner_or_worker(request.user)
        return obj.restaurant.check_owner(request.user)
