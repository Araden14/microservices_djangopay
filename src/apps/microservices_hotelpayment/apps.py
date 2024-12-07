from django.apps import AppConfig
from infrastructure.messaging.connection import RabbitMQConnectionManager
import os


class HotelPaymentConfig(AppConfig):
    name = 'apps.microservices_hotelpayment'
    verbose_name = "Hotel Payment"

    def ready(self):
        # Only run once in main process, not in reloader
        if os.environ.get('RUN_MAIN', None) != 'true':
            RabbitMQConnectionManager()