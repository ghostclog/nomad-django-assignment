from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class UsernameAuthentication(BaseAuthentication):
    def authenticate(self, request):
        X_USERNAME = request.headers.get("X-USERNAME")
        if not X_USERNAME:
            return None
        try:
            user = User.objects.get(username=X_USERNAME)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {X_USERNAME}")