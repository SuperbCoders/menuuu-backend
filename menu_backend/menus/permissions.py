"""
Проверка прав доступа пользователей к меню ресторанов
"""

from rest_framework import permissions

from menus.models import Menu
from restaurants.models import Restaurant


class MenuPermission(permissions.BasePermission):
    """
    Права доступа к меню. Опубликованное меню могут видеть все. Неопубликованное
    меню могут видеть администратор и работники ресторана, к которому относится
    меню. Они же могут редактировать меню.
    """

    def has_permission(self, request, view):
        """
        Просматривать меню имеют право все (неопубликованные меню скрыты от
        глаз посторонних пользователей в методе get_queryset соответствующего
        обработчика). При добавлении нового меню проверяется право пользователя
        редактировать меню соответствующего ресторана.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated or not request.user.is_active:
            return False
        if request.method == 'POST':
            # При добавлении нового меню придется извлекать идентификатор
            # ресторана из данных запроса и проверять права для него...
            restaurant_id = request.DATA['restaurant']
            if not Restaurant.objects.filter(pk=restaurant_id).exists():
                return False
            restaurant = Restaurant.objects.get(pk=restaurant_id)
            return restaurant.check_owner_or_worker(request.user)
        return request.user.is_staff or request.user.restaurant_staff.exists()

    def has_object_permission(self, request, view, obj):
        """
        Разрешаем редактировать меню пользователю, работающему в ресторане, с которым
        связано это меню или администратору. Если меню опубликовано то просматривать
        его могут все.
        """
        if obj.check_published() and request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or obj.check_restaurant_staff(request.user)


class MenuSectionPermission(permissions.BasePermission):
    """
    Права доступа к разделам меню. Они соответствуют правам доступа ко всему
    меню.
    """

    def has_permission(self, request, view):
        """
        Право на просмотр списка разделов меню или на добавление нового
        раздела меню.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated or not request.user.is_active:
            return False
        if request.method == 'POST':
            # При добавлении нового раздела придется извлекать идентификатор
            # меню из данных запроса и проверять права для него...
            menu_id = request.DATA['menu']
            if not Menu.objects.filter(pk=menu_id).exists():
                return False
            menu = Menu.objects.get(pk=menu_id)
            return menu.check_restaurant_staff(request.user)
        return request.user.is_staff or request.user.restaurant_staff.exists()

    def has_object_permission(self, request, view, obj):
        """
        Разрешаем редактировать раздел меню пользователю, работающему в ресторане,
        с которым связано это меню или администратору. Если меню опубликовано то
        просматривать его могут все.
        """
        if obj.check_published() and request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or obj.check_restaurant_staff(request.user)


class MenuCoursePermission(permissions.BasePermission):
    """
    Права доступа к блюдам. Они соответствуют правам доступа ко всему
    меню.
    """

    def has_permission(self, request, view):
        """
        Право на просмотр списка блюд или на добавление нового блюда.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated or not request.user.is_active:
            return False
        if request.method == 'POST':
            # При добавлении нового блюда придется извлекать идентификатор
            # меню из данных запроса и проверять права для него...
            menu_id = request.DATA['menu']
            if not Menu.objects.filter(pk=menu_id).exists():
                return False
            menu = Menu.objects.get(pk=menu_id)
            return menu.check_restaurant_staff(request.user)
        return request.user.is_staff or request.user.restaurant_staff.exists()

    def has_object_permission(self, request, view, obj):
        """
        Разрешаем редактировать блюда пользователю, работающему в ресторане,
        с которым связано меню, включающее это блюдо, или администратору. Если
        блюдо опубликовано то просматривать его могут все.
        """
        if obj.check_published() and request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or obj.check_restaurant_staff(request.user)
