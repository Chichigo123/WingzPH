from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

from .models import User


class UserAdmin(BasePermission):
    """
        Custom permission to only allow custom authenticated User and Django admin User to access the API
    """
    def has_permission(self, request, view):
        user = request.user
        if isinstance(user, User):
            return True
        elif isinstance(user, get_user_model()) and user.is_staff:
            return True
        return False
