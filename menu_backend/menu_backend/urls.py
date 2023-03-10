"""menu_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

from rest_framework import permissions, routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from menus.viewsets import MenuCourseViewSet, MenuSectionViewSet, MenuViewSet
from restaurants.viewsets import (
    RestaurantCategoryViewSet,
    RestaurantViewSet,
    RestaurantStaffViewSet
)
from restaurants.views import UnauthorizedRestaturantView
from tariffs.viewsets import TariffViewSet
from users.views import (
    UserCreationView,
    LoginView,
    LogoutView,
    MyRestaurantsView,
    MyProblemsView
)


router_v1 = routers.SimpleRouter()
router_v1.register('menu_courses', MenuCourseViewSet, basename='menucourse')
router_v1.register('menu_sections', MenuSectionViewSet, basename='menusection')
router_v1.register('menu', MenuViewSet, basename='menu')
router_v1.register('restaurant_categories', RestaurantCategoryViewSet, basename='restaurant_category')
router_v1.register('restaurants', RestaurantViewSet, basename='restaurant')
router_v1.register('restaurant_staff', RestaurantStaffViewSet, basename='restaurant_staff')
router_v1.register('tariffs', TariffViewSet, basename='tariff')


# Генерируем страницу с документацией по API
schema_view = get_schema_view(
   openapi.Info(
      title="Menu backend",
      default_version='v1',
      description=_("Menu service for restaurants"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    # Встроенная админка
    path('admin/', admin.site.urls),
    # Управление переводами строк через встроенную админку
    path('rosetta/', include('rosetta.urls')),
    # Регистрация нового пользователя
    path('api/v1/users/register/', UserCreationView.as_view(), name="user_register"),
    # Вход в систему
    path('api/v1/users/login/', LoginView.as_view(), name='user_login'),
    # Выход из системы
    path('api/v1/users/logout/', LogoutView.as_view(), name='user_logout'),
    # Получение пользователем списка ресторанов, которыми он владеет
    path('api/v1/users/my_restaurants/', MyRestaurantsView.as_view(), name='user_restaurants'),
    # Список проблем с данными о ресторанах, которыми владеет пользователь
    path('api/v1/users/my_problems/', MyProblemsView.as_view(), name='user_problems'),
    # Описание API
    path(
        'api/v1/swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger'
    ),
    # Получение меню ресторана неавторизованным пользователем
    path(
        'api/v1/public/restaurants/<pk>/',
        UnauthorizedRestaturantView.as_view(),
        name='public_restaurant'
    ),
    # API-обработчики для работы с данными по протоколу REST
    path('api/v1/', include(router_v1.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
