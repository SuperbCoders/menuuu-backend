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
                        title=_("Restaurant list"),
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
                                    title=_("Name and description"),
                                    description=_("The name and the description of the restaurant, in different languages"),
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'en': openapi.Schema(
                                            title=_("In English"),
                                            description=_("The name and the description of the restaurant, in English"),
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
                                    type=openapi.TYPE_STRING,
                                    format="slug"
                                ),
                                'logo': openapi.Schema(
                                    description=_("The restaurant's logo image URL"),
                                    type=openapi.TYPE_STRING,
                                    format="uri"
                                ),
                                'picture': openapi.Schema(
                                    description=_("The restaurant's picture URL"),
                                    type=openapi.TYPE_STRING,
                                    format="uri"
                                ),
                                'category': openapi.Schema(
                                    description=_("Restaurant's category ID"),
                                    type=openapi.TYPE_INTEGER
                                ),
                                'category_data': openapi.Schema(
                                    title=_("RestaurantCategory"),
                                    description=_("Restaurant's category data"),
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(
                                            description=_("Restaurant category primary key"),
                                            type=openapi.TYPE_INTEGER
                                        ),
                                        'translations': openapi.Schema(
                                            title=_("Category name"),
                                            desctiption=_("The name of the restaurant category, in different languages"),
                                            type=openapi.TYPE_OBJECT,
                                            properties={
                                                'en': openapi.Schema(
                                                    title=_("In English"),
                                                    description=_("The name of the restaurant category, in English"),
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
                                'country': openapi.Schema(
                                    description=_("Restaurant location country"),
                                    type=openapi.TYPE_STRING
                                ),
                                'city': openapi.Schema(
                                    description=_("Restaurant location city"),
                                    type=openapi.TYPE_STRING
                                ),
                                'street': openapi.Schema(
                                    description=_("Restaurant location street"),
                                    type=openapi.TYPE_STRING
                                ),
                                'building': openapi.Schema(
                                    description=_("Restaurant's building number"),
                                    type=openapi.TYPE_STRING
                                ),
                                'address_details': openapi.Schema(
                                    description=_("Restaurant address extra information (entrance number, floor, etc.)"),
                                    type=openapi.TYPE_STRING
                                ),
                                'zip_code': openapi.Schema(
                                    description=_("Restaurant's address ZIP code"),
                                    type=openapi.TYPE_STRING
                                ),
                                'longitude': openapi.Schema(
                                    description=_("Restaurant's location longitude"),
                                    type=openapi.TYPE_STRING,
                                    format="decimal"
                                ),
                                'latitude': openapi.Schema(
                                    description=_("Restaurant's location latitude"),
                                    type=openapi.TYPE_STRING,
                                    format="decimal"
                                ),
                                'phone': openapi.Schema(
                                    description=_("Restaurant's phone number"),
                                    type=openapi.TYPE_STRING,
                                    format="phone"
                                ),
                                'site': openapi.Schema(
                                    description=_("Restaurant's website URI"),
                                    type=openapi.TYPE_STRING,
                                    format="uri"
                                ),
                                'current_menu': openapi.Schema(
                                    title=_("Menu"),
                                    description=_("Currently published menu"),
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(
                                            description=_("Menu primary key"),
                                            type=openapi.TYPE_INTEGER
                                        ),
                                    }
                                )
                            },
                            required=['translations', 'stars', 'country', 'city', 'building', 'zip_code']
                        )
                    )
                }
            )
        ),
        401: openapi.Response("Not authenticated")
    }
)
