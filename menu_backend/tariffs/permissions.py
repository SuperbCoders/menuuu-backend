"""
Проверка прав доступа к тарифам.

Все пользователи, включая неавторизованных, могут читать информацию о тарифах.
Только администратор может изменять ее.
"""

from rest_framework import permissions


class TariffPermission(permissions.BasePermission):
    """
    Права доступа пользователей к тарифам. Позволяют любому пользователю
    просматривать информацию о тарифах и только администратору изменять
    ее.
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
        Проверка права на выполнения запроса request для тарифа obj
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated or not request.user.is_active:
            return False
        return request.user.is_staff
