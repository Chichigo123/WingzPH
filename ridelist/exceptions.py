# myapp/exceptions.py
from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call DRF's default exception handler to get the standard error response
    response = exception_handler(exc, context)

    # If DRF's handler returned a response, we can modify it
    if response is None and isinstance(exc, FieldError):
        return Response({"errors": exc.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    return response
