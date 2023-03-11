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


swagger_user_problems = swagger_auto_schema(
    operation_summary=_("Get the problem list"),
    operation_description=_("Get the list of problems of current user's restaurants"),
    responses={
        200: openapi.Response(
            "OK",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description=_("The number of the problems found")
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description=_("The list of the problems found"),
                        items=openapi.Items(
                            type=openapi.TYPE_STRING,
                            description=_("Problem description string")
                        )
                    )
                }
            )
        ),
        401: openapi.Response("Not authenticated")
    }
)


swagger_user_restaurants = swagger_auto_schema(
    operation_summary=_("Get my restaurant list"),
    operation_description=_("Get the list of the current user's restaurants."),
    responses={
        200: openapi.Response(
            "OK",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'count': openapi.Schema(
                        type=openapi.TYPE_INTEGER,
                        description=_("The number of the current user's restaurants")
                    ),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description=_("The list of the current user's restaurants"),
                        items=openapi.Items(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(
                                    description=_("Restaurant's primary key"),
                                    type=openapi.TYPE_INTEGER
                                ),
                                'translations': openapi.Schema(
                                    _("The name and the description of the restaurant, in different languages"),
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'en': openapi.Schema(
                                            _("The name and the description of the restaurant, in English"),
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'name': openapi.Schema(
                                                    description=_("Restaurant name in English"),
                                                    type=openapi.TYPE_STRING
                                                ),
                                                'description': openapi.Schema(
                                                    description=_("Restaurant description in English"),
                                                    type=openapi.TYPE_STRING
                                                ),
                                            }
                                        )
                                    }
                                ),
                                'slug': openapi.Schema(
                                    description=_("The short URL-friendly name of the restaurant (A-Z, 0-9 and - symbols only)"),
                                    type=openapi.TYPE_STRING
                                ),
                                'logo': openapi.Schema(
                                    description=_("The restaurant's logo image URL"),
                                    type=openapi.TYPE_STRING
                                ),
                                'picture': openapi.Schema(
                                    description=_("The restaurant's picture URL"),
                                    type=openapi.TYPE_STRING
                                ),
                                'category': openapi.Schema(
                                    description=_("Restaurant's category ID"),
                                    type=openapi.TYPE_INTEGER
                                ),
                                'category_data': openapi.Schema(
                                    _("Restaurant's category data"),
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(
                                            description=_("Restaurant category primary key"),
                                            type=openapi.TYPE_INTEGER
                                        ),
                                        'translations': openapi.Schema(
                                            _("The name of the restaurant category, in different languages"),
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'en': openapi.Schema(
                                                    _("The name of the restaurant category, in English"),
                                                    type=openapi.TYPE_OBJECT,
                                                    properties={
                                                        'name': openapi.Schema(
                                                            description=_("Restaurant category name in English"),
                                                            type=openapi.TYPE_STRING
                                                        ),
                                                    }
                                                )
                                            }
                                        ),
                                    }
                                ),
                                'stars': openapi.Schema(
                                    description=_("Number of stars, greater means better and more expensive"),
                                    type=openapi.TYPE_INTEGER
                                ),
                            }
                        )
                    )
                }
            )
        ),
        401: openapi.Response("Not authenticated")
    }
)
