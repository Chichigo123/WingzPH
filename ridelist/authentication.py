from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import User


class CustomHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Authenticate based on a custom header 'X-EMAIL' from User model
        email = request.META.get("HTTP_X_EMAIL")

        if not email:
            return None

        try:
            # Only Users with role='admin' can access the API
            user = User.objects.get(email=email, role=User.Roles.ADMIN)
        except User.DoesNotExist:
            raise AuthenticationFailed("No such user with admin priveleges.")

        return (user, None)
