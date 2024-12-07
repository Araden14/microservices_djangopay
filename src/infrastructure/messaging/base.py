#Base publisher for all publishers
from abc import ABC, abstractmethod
import json
from infrastructure.messaging.connection import RabbitMQConnectionManager

class BasePublisher(ABC):
    def __init__(self):
        self._connection_manager = RabbitMQConnectionManager()
    
    @property
    def channel(self):
        return self._connection_manager.get_channel()
        
    def publish(self, routing_key: str, message: dict):
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=json.dumps(message)
        )

class BaseConsumer:
    def __init__(self, queue_name):
        self._connection = RabbitMQConnectionManager()
        self.queue_name = queue_name
        
    def consume(self):
        self._connection.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self.process_message
        )
        self._connection.channel.start_consuming()