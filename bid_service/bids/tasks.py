import pika
from bid_service import settings
import json

def get_notification_content( status):
    """Генерирует текст уведомления в зависимости от статуса"""
    status_messages = {
        'accepted': 'Ваша заявка была одобрена!',
        'rejected': 'К сожалению, ваша заявка была отклонена.',
    }
    return status_messages.get(status, 'Статус вашей заявки был изменен.')

def send_notification(bid):
    """Отправка уведомления в RabbitMQ"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASSWORD
            )
        )
    )
    channel = connection.channel()
    
    # Объявляем очередь, если её нет
    channel.queue_declare(queue='notifications', durable=True)
    
    # Формируем сообщение
    message = {
        'to_user': bid.author_id,
        'user_email': bid.author_email,  # Предполагаем, что у User есть email
        'subject': 'Результат рассмотрения заявки',
        'content': get_notification_content(bid.status)
    }
    
    # Отправляем в очередь
    channel.basic_publish(
        exchange='',
        routing_key='notifications',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Сообщение persistent
        )
    )
    
    connection.close()