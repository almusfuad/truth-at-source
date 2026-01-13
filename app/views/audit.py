from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.models.audit import AuditLog



class AuditListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = AuditLog.objects.all().order_by('-timestamp')[:100]
        return Response([
            {
                "id": l.id,
                "actorUserId": l.actor_user_id,
                "actorRole": l.actor_role,
                "action": l.action,
                "objectType": l.object_type,
                "objectId": l.object_id,
                "metadata": l.metadata,
            } for l in logs
        ])