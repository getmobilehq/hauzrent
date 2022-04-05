from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('login/', views.user_login),
    path('admins/shipping/', views.shipping_admin),
    path('admins/bay/', views.bay_admin),
    path('otp/', views.otp_verification),
    path('otp/new/', views.reset_otp),
]
