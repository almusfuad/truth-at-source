from django.db import models
import json


class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    actor_user_id = models.CharField(max_length=50)
    actor_role = models.CharField(max_length=20)
    action = models.CharField(max_length=60)
    object_type = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50)
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']


    def set_metadata(self, data):
        self.metadata = json.dumps(data)

    def get_metadata(self):
        return json.loads(self.metadata or '{}') 