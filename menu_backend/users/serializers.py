"""
Сериализаторы данныз для регистрации пользователей в системе
"""

from users.models import User

from rest_framework import serializers


class UserCreationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания пользователей

    Известные проблемы
    ------------------
    *   В Сваггере поле пароля отображается в ответе, хотя его там не будет.
    """

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Создать нового пользователя"""
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            phone=validated_data['phone']
        )
        return user

    class Meta:
        model = User
        fields = ["username", "password", "email", "phone", "id"]
        write_only_fields = ["password"]
        read_only_fields = ["id"]

    password = serializers.CharField(write_only=True, required=True)
