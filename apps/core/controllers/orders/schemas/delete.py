from typing import Any

from drf_spectacular.utils import OpenApiParameter, inline_serializer
from rest_framework import serializers


def delete_schema() -> Any:
    return {
        "tags": ["Order"],
        "summary": "Delete an order",
        "description": (
            "Deletes an existing order record from the database. "
            "This operation cannot be undone."
        ),
        "parameters": [
            OpenApiParameter(
                name="id",
                type=str,
                location=OpenApiParameter.PATH,
                description="Order ID",
                required=True,
            ),
        ],
        "responses": {
            200: inline_serializer(
                name="OrderDeleteResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
            404: inline_serializer(
                name="OrderNotFoundResponse",
                fields={
                    "success": serializers.BooleanField(),
                    "message": serializers.CharField(),
                },
            ),
        },
    }

