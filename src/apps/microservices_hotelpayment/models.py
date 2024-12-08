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
    payment_id = models.UUIDField(primary_key=True, default=uuid4)
    reservation_id = models.UUIDField()
    client_id = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20)
    paymentmethod = models.CharField(max_length=20)

