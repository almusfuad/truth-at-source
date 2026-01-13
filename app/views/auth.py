import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import User


class LoginView(APIView):
    def post(self, request):
        user_id = request.data['userId']
        role = request.data['role']
        factory_id = request.data.get('factoryId')


        user, _ = User.objects.get_or_create(
            user_id=user_id,
            defaults={'role': role, 'factory_id': factory_id}
        )

        token = jwt.encode(
            {
                "user_id": user.user_id,
                "exp": datetime.utcnow() + timedelta(hours=24)
            },
            settings.SECRET_KEY,
            algorithm="HS256"
        )

        return Response({"token": token})
    
