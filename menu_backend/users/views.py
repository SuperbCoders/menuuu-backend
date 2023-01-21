"""
API для работы с пользователями - вход в систему, выход из системы, регистрация
"""

from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView

from users.models import User
from users.serializers import UserCreationSerializer


class UserCreationView(CreateAPIView):
    """
    Создание нового пользователя
    """
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserCreationSerializer
