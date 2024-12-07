from infrastructure.messaging.base import BasePublisher


#Payment initiated publisher
class PaymentInitiatedPublisher(BasePublisher):
    PAYMENT_INITIATED_QUEUE = 'payment_initiated'
    
    def __init__(self):
        super().__init__()
        self.declare_queues()
        
    def declare_queues(self):
        self.channel.queue_declare(queue=self.PAYMENT_INITIATED_QUEUE)

class PaymentEventPublisher(BasePublisher):
    PAYMENT_COMPLETED_QUEUE = 'payment_completed'
    PAYMENT_FAILED_QUEUE = 'payment_failed'
    
    def __init__(self):
        super().__init__()
        self.declare_queues()
    
    def declare_queues(self):
        self.channel.queue_declare(queue=self.PAYMENT_COMPLETED_QUEUE)
        self.channel.queue_declare(queue=self.PAYMENT_FAILED_QUEUE)
    
    def publish_payment_completed(self, payment_data: dict):
        self.publish(self.PAYMENT_COMPLETED_QUEUE, payment_data)