import pika
import json
import logging
from django.conf import settings
from users.models import User  # Assuming you have a User model

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)

def start_balance_updater_consumer():
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
    
    def callback(ch, method, properties, body):
        try:
            data = json.loads(body)
            user_id = data['user_id']
            amount = data['amount'],
            amount = amount[0]
            operation_type = data['type']
            value_type = data['value_type']
            if value_type == 'real':
                if operation_type == 'income':
                    user = User.objects.get(id=user_id)
                    user.balance += amount
                    user.balance_virtual += amount*0.01
                    user.save()
                else:
                    user = User.objects.get(id=user_id)
                    user.balance -= amount
                    user.balance_virtual += amount*0.1
                    user.save()
            else:
                if operation_type == 'income':
                    user = User.objects.get(id=user_id)
                    user.balance_virtual+=amount
                    user.save()
                else:
                    user = User.objects.get(id=user_id)
                    user.balance_virtual-=amount
                    user.save()
                    
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Updated balance for user_id={user_id}: +{amount} (real)")
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            # При необходимости можно не подтверждать сообщение, чтобы оно было переотправлено
    
    channel.basic_consume(
        queue='user_balance_updates',
        on_message_callback=callback
    )
    
    logger.info(' [*] Waiting for balance updates. To exit press CTRL+C')
    channel.start_consuming()
