from django.urls import path, include
from . import views

urlpatterns = [
    
    path('landlord/transaction/', views.transaction),
    path('landlord/transactions/', views.get_all_transactions),
    path('landlord/Confirm_payment', views.update_transaction),
    
    # The Tenant session is Captured in another App
    # path('tenant/initiate_transaction/', views.create_transaction),
    # path('tenant/transaction/', views.my_transactions),
]
