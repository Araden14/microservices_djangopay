from rest_framework.views import APIView
from rest_framework.response import Response
from .publishers.publishers import PaymentInitiatedPublisher

class PaymentView(APIView):
    def post(self, request):
        publisher = PaymentInitiatedPublisher()
        publisher.publish(
            routing_key=publisher.PAYMENT_INITIATED_QUEUE,
            message=request.data
        )
        return Response({'status': 'payment initiated'})