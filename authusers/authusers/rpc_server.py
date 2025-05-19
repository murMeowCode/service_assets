import pika
import json
import logging
from django.contrib.auth import get_user_model
import os

# Настройка логгера
logger = logging.getLogger('rpc_server')
logger.setLevel(logging.DEBUG)

# Форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Файловый обработчик
file_handler = logging.FileHandler('rpc_server.log')
file_handler.setFormatter(formatter)

# Консольный обработчик
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def on_request(ch, method, props, body):
    try:
        data = json.loads(body)
        user_id = data['user_id']
        logger.info(f"Received request for user_id: {user_id}")
        
        User = get_user_model()
        user = User.objects.get(pk=user_id)
        
        response = {
            'exists': True,
            'is_active': user.is_active,
            'username': user.username,
            'email': user.email,
            'is_root': user.is_root,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'father_name': user.father_name,
            'id': user.id,
            'vip_level': user.vip_level,
            'balance': user.balance,
            'balance_virtual': user.balance_virtual
        }
        
        logger.debug(f"User found: {response}")
        
    except User.DoesNotExist:
        response = {'exists': False}
        logger.warning(f"User not found: {user_id}")
    except Exception as e:
        response = {'error': str(e)}
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
    
    try:
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=json.dumps(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.debug(f"Response sent for user_id: {user_id}")
    except Exception as e:
        logger.critical(f"Failed to send response: {str(e)}", exc_info=True)

def start_server():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials('guest', 'guest'),
                heartbeat=600,
                blocked_connection_timeout=300
            )
        )
        channel = connection.channel()
        
        channel.queue_declare(queue='user_validation')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue='user_validation',
            on_message_callback=on_request
        )
        
        logger.info(" [x] RPC Server started. Awaiting requests...")
        channel.start_consuming()
        
    except pika.exceptions.AMQPConnectionError as e:
        logger.critical(f"Failed to connect to RabbitMQ: {str(e)}")
    except Exception as e:
        logger.critical(f"Server error: {str(e)}", exc_info=True)
    finally:
        if 'connection' in locals() and connection.is_open:
            connection.close()
            logger.info("Connection closed")

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authusers.settings')
    import django
    django.setup()
    start_server()
