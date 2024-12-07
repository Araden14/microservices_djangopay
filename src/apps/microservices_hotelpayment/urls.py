from django.contrib import admin
from django.urls import path
from apps.microservices_hotelpayment.views import PaymentView
from apps.microservices_hotelpayment.publishers.publishers import PaymentEventPublisher

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/initiate/', PaymentView.as_view(), name='initiate_payment'),
    path('payment/complete', PaymentEventPublisher, name='complete_payment'), 
    path('payment/failed', PaymentEventPublisher, name='failed_payment'),
]
