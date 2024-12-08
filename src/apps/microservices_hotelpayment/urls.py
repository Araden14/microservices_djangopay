from django.contrib import admin
from django.urls import path
from .views import create_payment, update_payment, delete_payment, generate_invoice, cancel_payment, get_payment, schema_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/create/', create_payment, name='create_payment'),
    path('payment/update/<uuid:reservation_id>/', update_payment, name='update_payment'),
    path('payment/delete/<uuid:reservation_id>/', delete_payment, name='delete_payment'),
    path('payment/invoice/<uuid:reservation_id>/', generate_invoice, name='generate_invoice'),
    path('payment/cancel/<uuid:reservation_id>/', cancel_payment, name='cancel_payment'),
    path('payment/<uuid:reservation_id>/', get_payment, name='get_payment'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
