from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .serializers import ApartmentSerializer
from .models import Apartment
from accounts.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsLandlord, IsTenant, IsAdmin
from rest_framework.exceptions import PermissionDenied

import cloudinary
# Create your views here.

User = get_user_model()


@api_view(["POST"])
@permission_classes(IsLandlord)
def create_apartment(request):

    if request.method == "POST":
        if request.user.role == "landlord":
            serializer = ApartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                return Response({"message":"Saved Succefully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":serializer.errors,"message":"failed"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@permission_classes([IsLandlord])
def get_all_apartments(request):        
    if request.method == "GET":
        apartments = Apartment.objects.filter(user=request.user)
        serializer = ApartmentSerializer(apartments, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsLandlord])
def apartment(request, pk):        
    if request.method == "GET":
        apartment = Apartment.objects.get(id=pk)
        serializer = ApartmentSerializer(apartment, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        apartment = Apartment.objects.get(id=pk)
        serializer = ApartmentSerializer(instance=apartment, data = request.data) 

        if serializer.is_valid():    
            serializer.save()

            data = {
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {

               'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    #delete the account
    elif request.method == 'DELETE':
        apartment = Apartment.objects.get(id=pk)
        apartment.delete()


        return Response({}, status = status.HTTP_204_NO_CONTENT)