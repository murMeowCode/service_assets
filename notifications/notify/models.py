from django.db import models

class Notification(models.Model):
    seen = models.BooleanField(default=False)
    to_user = models.IntegerField(null=False)
    user_email = models.TextField(null=True)
    subject = models.TextField(max_length=100)
    content = models.TextField(max_length=500)

