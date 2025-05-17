# tasks.py
from celery import shared_task
from django.apps import apps
from django.core.mail import send_mail
from notifications.settings import EMAIL_HOST_USER
import logging

@shared_task(bind=True, name='notify.tasks.process_notification')
def process_notification(self, message):
    try:
        Notification = apps.get_model('notify', 'Notification')
        
        notification = Notification.objects.create(
            user_email=message['user_email'],
            to_user=message['to_user'],
            subject=message['subject'],
            content=message['content'],
            seen=False
        )

        send_mail(
            message['subject'],
            message['content'],
            EMAIL_HOST_USER,
            [message['user_email']],
            fail_silently=False,
        )
        return f"Notification {notification.id} sent"
        
    except KeyError as e:
        logging.error(f"Missing key in message: {e}")
        raise self.retry(exc=e, countdown=60)
    except Exception as e:
        logging.error(f"Notification error: {e}")
        raise self.retry(exc=e, countdown=120)