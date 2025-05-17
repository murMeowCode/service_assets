import pika
import uuid
import json

class AuthRPCClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',  # или '127.0.0.1'
                port=5672,
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        self.channel = self.connection.channel()
        
        # Создаем временную очередь для ответов
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        
        # Подписываемся на ответы
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, user_id):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        
        self.channel.basic_publish(
            exchange='',
            routing_key='user_validation',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps({'user_id': str(user_id)})
        )
        
        # Ждем ответа с таймаутом
        while self.response is None:
            self.connection.process_data_events(time_limit=2)  # Таймаут 2 секунды
            if self.response is None:
                raise TimeoutError("Auth service timeout")
        
        return self.response