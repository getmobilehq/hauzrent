from django.urls import path, include
from . import views

urlpatterns = [
    
    path('landlord/apartment/new', views.create_apartment),
    path('landlord/apartment/', views.apartment),
    path('landlord/apartments/', views.get_all_apartments),
    
]
