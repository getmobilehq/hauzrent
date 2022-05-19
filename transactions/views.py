from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
import transactions

from .serializers import TransactionSerializer
from .models import Transaction
from accounts.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsLandlord, IsTenant, IsAdmin
from rest_framework.exceptions import PermissionDenied

import cloudinary
# Create your views here.

User = get_user_model()

# (This is a Tenant PART CODE whcih is likely not going to be included in this Particular APP)
# @api_view(["POST"])
# @permission_classes(IsTenant)
# def create_transaction(request):

#     if request.method == "POST":
#         if request.user.role == "tenant":
#             serializer = TransactionSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
                
#                 return Response({"message":"Payment Initiated, Wait for Confirmation"}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"error":serializer.errors,"message":"failed (Please fill correctly)"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@permission_classes([IsLandlord])
def get_all_transactions(request):        
    if request.method == "GET":
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transaction, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsLandlord])
def transaction(request, pk):        
    if request.method == "GET":
        transaction = Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(transaction, many=True)
        data = {"message":"success",
                "data":serializer.data}
        
        return Response(data,status=status.HTTP_200_OK)

    elif request.method == 'POST':
        transaction = Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(instance=transaction, data = request.data) 

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

    #delete the transaction
    elif request.method == 'DELETE':
        transaction = Transaction.objects.get(id=pk)
        transaction.delete()


        return Response({}, status = status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsLandlord])
def update_transaction(request, pk): 
    if request.method == 'POST':
        transaction = Transaction.objects.get(id=pk)
        transaction.status = Transaction.status.get(status)
        serializer = TransactionSerializer(instance=transaction, data = request.data) 