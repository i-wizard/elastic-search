from typing import Dict

from django.utils import dateparse
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .exceptions import CustomAPIException

class HttpSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http"]
        return schema
    
class ResponseManager:
    """Utility class that abstracts how a DRF response is created"""

    @staticmethod
    def handle_response(
        data: Dict = {}, errors: Dict = {}, status: int = 200, message: str = ""
    ) -> Response:
        if errors:
            return Response({"errors": errors, "message": message, "status":"error"}, status=status)
        return Response({"data": data, "message": message, "status":"success"}, status=status)

    @staticmethod
    def handle_paginated_response(
        paginator_instance: PageNumberPagination = PageNumberPagination(),
        data: Dict = {},
    ) -> Response:
        return paginator_instance.get_paginated_response(data)

class CustomPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "data": data,
                "status":"success",
                "message":"Data retrieved successfully"
            }
        )


def paginate_response(
    queryset, serializer_, request, paginator=CustomPagination
):  
    max_page_size = 20
    min_page_size = 1
    page_size = min(int(request.GET.get("page_size", 10)), max_page_size)
    paginator_instance = paginator()
    paginator_instance.page_size = max(page_size, min_page_size)
    return ResponseManager.handle_paginated_response(
        paginator_instance,
        serializer_(
            paginator_instance.paginate_queryset(queryset, request), many=True
        ).data,
    )
class Validators:
    @staticmethod
    def is_valid_date_format(date):
        """
        Validate that a date is in the correct format
        """

        if date:
            date_value = dateparse.parse_date(date)
            if not date_value:
                raise CustomAPIException(
                    detail="Date format is incorrect. Use YYYY-MM-DD",
                    status_code=400,
                )
            return True
    
    @staticmethod  
    def is_start_date_less_than_or_equals_end_date(start_date, end_date):
        """
        Validate that the end date is greater than or equal to the start date
        """
        if not start_date or not end_date:
            return False
        start_date = dateparse.parse_date(start_date)
        end_date = dateparse.parse_date(end_date)

        if end_date >= start_date:
            return True

        raise CustomAPIException(
            detail="The end date should be greater than or equal to the start date.",
            status_code=400,
        )
