import json
from celery import shared_task
from .models import Notification
from django.core.mail import send_mail
from notifications.settings import EMAIL_HOST_USER

@shared_task
def process_notification(message):
    data = json.loads(message)
    Notification.objects.create(
        user_email = data['user_email'],
        to_user=data['to_user'],
        subject=data['subject'],
        content=data['content'],
        seen=False
    )

    send_mail(
            data['subject'],
            data['content'],
            EMAIL_HOST_USER,
            data['user_email'],
            fail_silently=False,
        )
