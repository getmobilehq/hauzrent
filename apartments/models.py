from django.db import models
import uuid
from django.contrib.auth import get_user_model

User=get_user_model()
# User Model


# Apartments models here.
class Apartment(models.Model):
    House_Type = (
    ('bungalow','Bungalow'),
    ('Two_Bedroom','Two Bedroom Duplex'),
    ('Three_Bedroom','Three Bedroom Flat'),
    ('others', 'Others'),
    )
    #PROPERTY
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    type = models.CharField(max_length=300, default="others", choices=House_Type)
    address = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    image_url1 = models.URLField()
    image_url2 = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=100, choices=House_Type)
    landlord = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    tenant = models.ForeignKey('Tenant', blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(max_length=400, blank=True, null=True)
    Rent_Amount = models.CharField(max_length=50, default = '#50,000', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.type)



    

