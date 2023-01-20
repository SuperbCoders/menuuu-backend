"""
Встроенная документация для API-обработчиков для работы с ресторанами
"""

from django.utils.translation import gettext_lazy as _

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


swagger_public_menu = swagger_auto_schema(
    operation_name=_("Get the menu"),
    operation_description=_("Get the current menu for the specified restaurant"),
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description="The primary key of the restaurant",
            type=openapi.TYPE_INTEGER,
            required=True
        ),
        openapi.Parameter(
            'language',
            openapi.IN_QUERY,
            description="Return the menu at this language",
            type=openapi.TYPE_STRING,
            required=False
        ),
    ],
    responses = {
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description=_("The identified of the restaurant (same with 'id' parameter)")
                ),
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("The name of the restaurant")
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("The description of the restaurant")
                ),
                'phone': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("The contact phone number of the restaurant")
                ),
                'site': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("The restaurant's site url")
                ),
                'logo': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("The URL of restaurant's logo image, if available")
                ),
                'picture': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("The URL of restaurant's picture, if available")
                ),
                'stars': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description=_("Number of stars. Greater value means greater quality and greater prices. Worst value is 1 while the value 0 means information is not available.")
                ),
                'category': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description=_("Restaurant category"),
                    properties={
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Category name. It may be somewhat like 'italian', 'chinese', etc."),
                        )
                    }
                ),
                'address': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description=_("Restaurant address"),
                    properties={
                        'country': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Country name")
                        ),
                        'city': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("City name")
                        ),
                        'street': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Street name")
                        ),
                        'building': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Building number")
                        ),
                        'address_details': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Address details like entrance number, level number, etc.")
                        ),
                        'zip_code': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Zip/postal code")
                        ),
                        'latitude': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description=_("Latitude if available")
                        ),
                        'longitude': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            description=_("Longitude if available")
                        )
                    }
                ),
                'menu': openapi.Schema(
                    description=_("Restaurant's menu"),
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'title': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Menu title")
                        )
                    }
                )
            }
        ),
        404: "Restaurant not found"
    }
)
