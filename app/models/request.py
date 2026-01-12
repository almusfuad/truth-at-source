from django.db import models

class Request(models.Model):
    factory_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='requests'
    )



class RequestItem(models.Model):
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='items'
    )
    doc_type = models.CharField(max_length=100)
    fulfilled_evidence = models.ForeignKey(
        'Evidence',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='fulfilled_requests'
    )
    fulfilled_version = models.ForeignKey(
        'Version',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='fulfilled_requests'
    )
