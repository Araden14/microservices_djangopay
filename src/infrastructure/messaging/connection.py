import pika
from django.conf import settings
import threading
import logging

logger = logging.getLogger(__name__)

class RabbitMQConnectionManager:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, 'connection'):
            self.connection = None
            self.channel = None
            self.connect()
            
    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    credentials=pika.PlainCredentials(
                        settings.RABBITMQ_USER,
                        settings.RABBITMQ_PASS
                    ),
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            self.channel = self.connection.channel()
            # Enable publisher confirms
            self.channel.confirm_delivery()
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}")
            raise e

    def declare_queue(self, queue_name, durable=True, dead_letter_exchange=None):
        """
        Declare a queue with optional dead letter queue
        """
        arguments = {}
        if dead_letter_exchange:
            arguments['x-dead-letter-exchange'] = dead_letter_exchange
            
        self.channel.queue_declare(
            queue=queue_name,
            durable=durable,  # Survive broker restart
            arguments=arguments
        )
        
    def publish_message(self, queue_name, message, persistent=True):
        """
        Publish message to queue with confirmation
        """
        try:
            properties = pika.BasicProperties(
                delivery_mode=2 if persistent else 1,  # Make message persistent
            )
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=message,
                properties=properties,
                mandatory=True  # Message must be routable
            )
        except Exception as e:
            logger.error(f"Error publishing message: {e}")
            raise e

    def consume_message(self, queue_name, callback, prefetch_count=1):
        """
        Set up consumer with automatic acknowledgment
        """
        # Set QoS prefetch count
        self.channel.basic_qos(prefetch_count=prefetch_count)
        
        # Start consuming
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=False  # Manual acknowledgment
        )
        
    def start_consuming(self):
        """
        Start consuming messages
        """
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            
    def get_channel(self):
        if not self.connection or self.connection.is_closed:
            self.connect()
        return self.channel