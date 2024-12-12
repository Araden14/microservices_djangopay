#Models for the hotel payment service
from django.db import models
from uuid import uuid4


#Base model
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Payment(BaseModel):
    payment_id = models.CharField(max_length=24, primary_key=True)
    reservation_id = models.CharField(max_length=24)
    client_id = models.CharField(max_length=24)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)
    paymentmethod = models.CharField(max_length=20)

