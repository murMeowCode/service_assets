import os
from celery import Celery
import pika
import json
from notify.tasks import process_notification
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifications.settings')

app = Celery('notifications')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['notify']) 
