from typing import Dict, List, Union

from django.utils.encoding import force_str
from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = (
        "We are unable to process your request at this time. Please try again."
    )

    def __init__(self, detail: Union[List, Dict, str], status_code: int) -> None:
        self.status_code = status_code if status_code else self.status_code
        message = detail if detail is not None else self.default_message
        self.detail = {"message": force_str(message)}

