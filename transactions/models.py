from django.db import models
import uuid
from django.contrib.auth import get_user_model

User=get_user_model()
# User Model


# Transactions models here.
class Transaction(models.Model):
    Payment = (
    ('completed','Completed'),
    ('not_paid','Not_paid'),
    ('half_paid','Half_paid'),
    )
    #PROPERTY
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    amount = models.CharField(max_length=300, default="others")
    initiator = models.ForeignKey('Tenant', blank=True, null=True, on_delete=models.CASCADE)
    Confirmed = models.CharField(max_length=50)
    transaction_image = models.URLField()
    status = models.CharField(max_length=100, choices=Payment, default='not_paid')
    recevier = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=400, blank=True, null=True)


    def __str__(self):
        return str(self.type)



    

