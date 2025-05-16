import pika
import json
from django.contrib.auth import get_user_model
import os

# Подключение к Django ORM
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authusers.settings')
import django


def on_request(ch, method, props, body):
    User = get_user_model()
    try:
        data = json.loads(body)
        user_id = data['user_id']
        
        user = User.objects.get(pk=user_id)
        response = {
            'exists': True,
            'is_active': user.is_active,
            'username': user.username,
            'email': user.email,
            'role':user.role,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'father_name':user.father_name,
            'id':user.id
        }
    except User.DoesNotExist:
        response = {'exists': False}
    except Exception as e:
        response = {'error': str(e)}
    
    # Отправка ответа
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=json.dumps(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_server():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',  # или '127.0.0.1'
            port=5672,
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    channel = connection.channel()
    
    channel.queue_declare(queue='user_validation')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='user_validation',
        on_message_callback=on_request
    )
    
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()

if __name__ == '__main__':
    start_server()