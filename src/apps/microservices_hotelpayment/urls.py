from django.contrib import admin
from django.urls import path
from .views import create_payment, update_payment, delete_payment, generate_invoice, cancel_payment, get_payment, schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Hotel Payment API",
      default_version='v1',
      description="API documentation for Hotel Payment Service",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   url=f'http://localhost:8000',  # Add your base URL here
)
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
