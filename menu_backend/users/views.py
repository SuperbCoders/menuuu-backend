"""
API для работы с пользователями - вход в систему, выход из системы, регистрация
"""

import logging

from django.contrib.auth import authenticate, logout
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer

from users.models import User
from users.swagger import swagger_login, swagger_logout
from users.serializers import UserCreationSerializer


class UserCreationView(CreateAPIView):
    """
    Создание нового пользователя
    """
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserCreationSerializer


class LoginView(APIView):
    """
    Вход пользователя в систему по логину и паролю

    Пример запроса
    --------------
    {
        'username': 'admin',
        'password': 'verysecretpass'
    }

    Пример ответа при удачном входе в систему
    -----------------------------------------
    {
        'user': 1,
        'token': 'verysecrettoken'
    }
    """

    permission_classes = [AllowAny]
    http_method_names = ['post', 'options']

    @swagger_login
    def post(self, request):
        """Вход пользователя в систему"""
        logger = logging.getLogger('default')
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response(
                {'detail': _("Username and password must be provided")},
                status=400
            )
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            logger.info(f"The user '{username}' logged in")
            return Response(
                {
                    'detail': _("Successfully logged in"),
                    'user': user.pk,
                    'token': token.key
                },
                status=200
            )
        logger.info(f"The user '{username}' tried to log in with an invalid password")
        return Response(
            {'detail': _("Incorrect username or password")},
            status=403
        )


class LogoutView(APIView):
    """
    Выход пользователя из системы.

    Осуществляется запросом POST без параметров
    """
    http_method_names = ['post', 'options']
    permission_classes = [IsAuthenticated]

    @swagger_logout
    def post(self, request):
        """Выход пользователя из системы"""
        logger = logging.getLogger('default')
        key = request.META.get('HTTP_AUTHORIZATION')
        if key.startswith('Token'):
            key = key[5:]
        key = key.strip()
        Token.objects.filter(key=key, user=request.user).all().delete()
        logger.info(f"The user '{request.user.username}' logged out")
        logout(request)
        return Response({'detail': _("Successfully logged out")}, status=200)


class MyRestaurantsView(APIView):
    """
    Список ресторанов, которыми владеет текущий пользователь.
    """
    http_method_names = ['get', 'head', 'options']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Получение пользователем списка своих ресторанов"""
        user = self.request.user
        restaurant_ids = set(
            user.restaurant_staff.filter(position='owner').values_list(
                'restaurant_id', flat=True
            )
        )
        restaurants = Restaurant.objects.filter(id__in=restaurant_ids).all()
        results = [RestaurantSerializer(item).data for item in restaurants]
        return Response(
            {
                'count': len(results),
                'results': results
            },
            status=200
        )


class MyProblemsView(APIView):
    """
    Список проблем с данными о ресторанах, которыми владеет текущий пользователь
    """
    http_method_names = ['get', 'head', 'options']
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Получение пользователем списка своих ресторанов"""
        user = self.request.user
        restaurant_ids = set(
            user.restaurant_staff.filter(position='owner').values_list(
                'restaurant_id', flat=True
            )
        )
        restaurants = Restaurant.objects.filter(id__in=restaurant_ids).all()
        problems = []
        for restaurant in restaurants:
            problems += restaurant.get_problems()
        return Response(
            {
                'count': len(problems),
                'results': problems
            },
            status=200
        )
