"""
Документация для обработчиков входа пользователя в систему и выхода
из системы
"""

from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


swagger_login = swagger_auto_schema(
    operation_summary=_("Log in"),
    operation_description=_("Log in with username and password"),
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties = {
            'username': openapi.Schema(
                type=openapi.TYPE_STRING,
                description=_("Username")
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_STRING,
                description=_("Password")
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
                        description=_("Success message")
                    ),
                    'user': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description=_("User id")
                    ),
                    'token': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=_("Access token")
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
                        description=_("Error message - username or password not provided")
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
                        description=_("Error message - incorrect username or password")
                    ),
                }
            )
        )
    }
)


swagger_logout = swagger_auto_schema(
    operation_summary=_("Log out"),
    operation_description=_("Log out the current user"),
    responses={
        200: openapi.Response(
            "OK",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=_("Message: successfully logged out")
                    ),
                }
            )
        ),
        401: openapi.Response("Not authenticated")
    }
)
