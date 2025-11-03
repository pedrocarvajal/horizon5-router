from typing import Any

from drf_spectacular.utils import inline_serializer
from rest_framework import serializers

from apps.core.schemas.pagination import pagination_schema
from apps.core.schemas.responses import response_200_schema


def get_schema() -> Any:
    return {
        "tags": ["Report Performance"],
        "summary": "Get report performance data",
        "description": (
            "Provides a list of report performance records saved on the database, "
            "and also allows to filter the results by various parameters."
        ),
        "parameters": [
            *pagination_schema(),
        ],
        "responses": {
            **response_200_schema(
                "ReportPerformanceController",
                {
                    "data": inline_serializer(
                        name="ReportPerformance",
                        fields={
                            "id": serializers.CharField(),
                            "report_id": serializers.CharField(),
                            "value": serializers.FloatField(),
                            "date": serializers.DateTimeField(),
                            "created_at": serializers.DateTimeField(),
                            "updated_at": serializers.DateTimeField(),
                        },
                    ),
                },
            ),
        },
    }

