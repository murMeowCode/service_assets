# services/rabbitmq_service.py
import pika
import json
from django.conf import settings
from lottery_service.rpc_client import AuthRPCClient

def get_notification_content(status):
    """Генерирует текст уведомления в зависимости от статуса"""
    status_messages = {
        'winner': 'Вы выиграли супер-приз лотереи!',
        'partial_winner': 'Вы стали победителем лотереи!',
        'loser': 'К сожалению, на этот раз Вы не выиграли в лотерее.',
    }
    return status_messages.get(status, 'Статус вашей заявки был изменен.')

class RabbitMQService:
    @staticmethod
    def send_balance_update(user_id, amount, opearation_type, value_type):
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
        
        channel.queue_declare(queue='user_balance_updates', durable=True)
        
        message = {
            'user_id': int(user_id),
            'amount': float(amount),
            'type': opearation_type,
            'value_type': value_type,
        }

        channel.basic_publish(
            exchange='',
            routing_key='user_balance_updates',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
                content_type='application/json',
                content_encoding='utf-8'
            )
        )
        connection.close()

    @staticmethod
    def send_notification(part_instance):
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
        rpc_client = AuthRPCClient()
        response = rpc_client.call(part_instance.user_id)
        # Формируем сообщение
        message = {
            'task': 'notify.tasks.process_notification',  # Указываем полный путь к задаче
            'args': [{
                'to_user': part_instance.user_id,
                'user_email': response['email'],
                'subject': 'Результат проведения лотереи',
                'content': get_notification_content(part_instance.status)
            }],
            'kwargs': {}
        }

        channel.basic_publish(
            exchange='notifications',  # Должно соответствовать обменнику в Celery
            routing_key='notifications',  # Должно соответствовать routing_key в Celery
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Сообщение persistent
            )
        )
        
        connection.close()
        
