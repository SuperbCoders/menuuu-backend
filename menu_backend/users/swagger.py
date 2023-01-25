"""
Документация для обработчиков входа пользователя в систему и выхода
из системы
"""

from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


swagger_login = swagger_auto_schema(
    operation_summary=_("Вход пользователя в систему"),
    operation_description=_("Вход в систему по имени пользователя и паролю"),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties = {
            'username': openapi.Schema(
                type=openapi.TYPE_STRING,
                description=_("Имя пользователя")
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description=_("Пароль пользователя")
            ),
        }
    ),
    responses = {
        200: openapi.Response(
            "OK",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=_("Сообщение об успешном входе")
                    ),
                    'user': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description=_("Идентификатор пользователя")
                    ),
                    'token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=_("Токен доступа")
                    )
                }
            )
        ),
        400: openapi.Response(
            "Bad request",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=_("Сообщение об ошибке - неверный формат запроса")
                    ),
                }
            )
        ),
        403: openapi.Response(
            "Forbidden",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=_("Сообщение об ошибке - неправильный пароль")
                    ),
                }
            )
        )
    }
)
