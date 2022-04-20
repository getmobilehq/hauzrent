from rest_framework import serializers
from .model import Apartment

class ApartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Apartment
        fields = '__all__'
        