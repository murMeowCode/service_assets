from django.db import models


class Status(models.TextChoices):
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
    PENDING = 'pending', 'Pending'

class Bid(models.Model):
    author_id = models.IntegerField()
    author_email = models.TextField(max_length=50)
    status = models.CharField(choices=Status.choices,default=Status.PENDING)
    created_at = models.DateTimeField(auto_now=True)
    payload = models.TextField(max_length=100) # Замените на свою логику заявок
