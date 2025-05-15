import os
from celery import Celery
import pika
from notify.tasks import process_notification

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifications.settings')

app = Celery('notifications')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['notify']) 

@app.task
def consume_notifications():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications', durable=True) 
    
    def callback(ch, method, properties, body):
        # Измените вызов задачи
        message = body.decode('utf-8')
        app.send_task(
            'notify.tasks.process_notification',
            args=[message],
            queue='notifications'
        )
    
    channel.basic_consume(
        queue='notifications',
        on_message_callback=callback,
        auto_ack=True
    )
    channel.start_consuming()