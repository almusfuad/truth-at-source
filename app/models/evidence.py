from django.db import models


class Evidence(models.Model):
    name = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=100)
    expiry = models.DateField()
    notes = models.TextField(blank=True, null=True)
    factory_id = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='evidences'
    )


    def __str__(self):
        return f"{self.name} ({self.doc_type})"
    

    class Meta:
        unique_together = ('name', 'factory_id')
    


class Version(models.Model):
    evidence = models.ForeignKey(
        Evidence,
        on_delete=models.CASCADE,
        related_name='versions'
    )
    version_id = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    expiry = models.DateField()

    class Meta:
        ordering = ['-id']
