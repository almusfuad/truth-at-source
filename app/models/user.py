from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('factory', 'Factory')
    ]

    user_id = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    factory_id = models.CharField(max_length=50, blank=True, null=True)


    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return f"{self.user_id} ({self.role})"
    