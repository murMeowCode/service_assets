import json
from celery import shared_task
from django.apps import apps
from django.core.mail import send_mail
from notifications.settings import EMAIL_HOST_USER

@shared_task(name='notify.tasks.process_notification')
def process_notification(message):
    Notification = apps.get_model('notify', 'Notification')

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
            [data['user_email']],
            fail_silently=False,
        )
