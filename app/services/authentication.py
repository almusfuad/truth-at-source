import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app.models import User


class SimpleJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        header = request.headers.get('Authorization')
        if not header or not header.startswith('Bearer '):
            return None
        
        token = header.split()[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        
        user = User.objects.filter(user_id=payload['user_id'])
        return (user, None)
    