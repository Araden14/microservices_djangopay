from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Payment
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
import io
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import time
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_description="Create a new payment",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['reservation_id', 'client_id', 'amount', 'currency', 'status', 'paymentmethod'],
        properties={
            'reservation_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
            'client_id': openapi.Schema(type=openapi.TYPE_STRING, format='uuid'),
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER),
            'currency': openapi.Schema(type=openapi.TYPE_STRING),
            'paymentmethod': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={
        201: openapi.Response(
            description="Payment created successfully",
            examples={"application/json": {"status": "Payment successful"}}
        ),
        400: openapi.Response(
            description="Bad request",
            examples={"application/json": {"error": "Missing required field"}}
        )
    }
)
@csrf_exempt
@api_view(['POST'])
def create_payment(request):
    try:
        data = request.data 
        payment = Payment(
            reservation_id=data['reservation_id'],
            client_id=data['client_id'],
            amount=data['amount'],
            currency=data['currency'],
            status='Confirmed',
            paymentmethod=data['paymentmethod']
        )
        print("Processing payment...")
        time.sleep(10)
        print("Payment processed : success")

        payment.save()
        return Response({'status': 'payment created'}, status=status.HTTP_201_CREATED)
    except KeyError as e:
        return Response(
            {'error': f'Missing required field: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

#Get all payments
@swagger_auto_schema(
    method='get',
    operation_description="Get all payments",
    responses={
        200: openapi.Response(
            description="List of all payments",
            examples={"application/json": [{"payment_id": "uuid", "reservation_id": "id", "client_id": "id", "amount": 100.00, "currency": "EUR", "status": "Confirmed", "paymentmethod": "card"}]}
        )
    }
)
@csrf_exempt
@api_view(['GET'])
def get_all_payments(request):
    payments = Payment.objects.all()
    payment_list = []
    for payment in payments:
        payment_list.append({
            'payment_id': payment.payment_id,
            'reservation_id': payment.reservation_id,
            'client_id': payment.client_id,
            'amount': payment.amount,
            'currency': payment.currency,
            'status': payment.status,
            'paymentmethod': payment.paymentmethod
        })
    return Response(payment_list, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['PUT'])
def update_payment(request, reservation_id):
    try:
        payment = Payment.objects.get(reservation_id=reservation_id)
        data = request.data
        
        payment.client_id = data.get('client_id', payment.client_id)
        payment.amount = data.get('amount', payment.amount)
        payment.currency = data.get('currency', payment.currency)
        payment.status = data.get('status', payment.status)
        payment.paymentmethod = data.get('paymentmethod', payment.paymentmethod)
        
        payment.save()
        return Response({'status': 'payment updated'}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['DELETE'])
def delete_payment(request, reservation_id):
    try:
        payment = Payment.objects.get(reservation_id=reservation_id)
        payment.delete()
        return Response({'status': 'payment deleted'}, status=status.HTTP_204_NO_CONTENT)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['GET'])
def generate_invoice(request, reservation_id):
    try:
        payment = Payment.objects.get(reservation_id=reservation_id)
        
        # Create a file-like buffer to receive PDF data
        buffer = io.BytesIO()
        
        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Draw invoice content
        p.drawString(100, 750, "INVOICE")
        p.drawString(100, 700, f"Payment ID: {payment.payment_id}")
        p.drawString(100, 675, f"Reservation ID: {payment.reservation_id}")
        p.drawString(100, 650, f"Client ID: {payment.client_id}")
        p.drawString(100, 625, f"Amount: {payment.amount} {payment.currency}")
        p.drawString(100, 600, f"Payment Method: {payment.paymentmethod}")
        p.drawString(100, 575, f"Status: {payment.status}")
        
        # Close the PDF object
        p.showPage()
        p.save()
        
        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'invoice_{payment.payment_id}.pdf')
        
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
@csrf_exempt
@api_view(['PUT'])
def cancel_payment(request, reservation_id):
    try:
        payment = Payment.objects.get(reservation_id=reservation_id)
        payment.status = "Cancelled"
        payment.save()
        return Response({'status': 'payment cancelled'}, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['GET'])
def get_payment(request, reservation_id):
    try:
        payment = Payment.objects.get(reservation_id=reservation_id)
        return Response({
            'payment_id': payment.payment_id,
            'reservation_id': payment.reservation_id,
            'client_id': payment.client_id,
            'amount': payment.amount,
            'currency': payment.currency,
            'status': payment.status,
            'payment_method': payment.paymentmethod
        }, status=status.HTTP_200_OK)
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'},
            status=status.HTTP_404_NOT_FOUND
        )



schema_view = get_schema_view(
   openapi.Info(
      title="Microservice de paiement et de facturation de l'hotel",
      default_version='v1',
      description="API pour les opérations de paiement et de facturation de l'hotel",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
