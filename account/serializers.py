from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from config import settings
from .models import OTP, ResetPasswordOTP, User
from django.contrib.auth import password_validation
import random
from django.utils import timezone
from django.core.mail import send_mail

def generate_otp(n):
    return "".join([random.choice(['0','1','2','3','4','5','6','7','8','9']) for _ in range(n)])

url='#'

class UserSerializer(serializers.ModelSerializer):
    self_storages = serializers.ReadOnlyField()
    customer_to_customer = serializers.ReadOnlyField()
    payment_history = serializers.ReadOnlyField()
    customer_to_courier = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    parcel_stats=serializers.ReadOnlyField()
    saved_cards = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'phone', 'role','password', 'address','profile_pics', 'logistic_partner','profile_pics_url','firebase_key','date_joined', 'self_storages', 'customer_to_customer', 'customer_to_courier','payment_history', 'parcel_stats', 'saved_cards']
        
    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

     
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password  = serializers.CharField(max_length=200)
    new_password  = serializers.CharField(max_length=200)
    confirm_password  = serializers.CharField(max_length=200)
    
    
    def check_pass(self):
        """ checks if both passwords are the same """
        if self.validated_data['new_password'] != self.validated_data['confirm_password']:
            raise serializers.ValidationError({"error":"Please enter matching passwords"})
        return True
            
class ChangeRoleSerializer(serializers.Serializer):
    role = serializers.CharField()
    

  
class ResetPasswordOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
     
    def get_otp(self):
        try:
            user = User.objects.get(email=self.validated_data['email'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='There is no active user with this email')
        
        code = generate_otp(6)
        expiry_date = timezone.now() + timezone.timedelta(minutes=10)

        ResetPasswordOTP.objects.create(code=code, email=self.validated_data['email'], user=user, expiry_date=expiry_date )
        
        return {'message': 'Please check your email for OTP.'}
        
        
        
class ConfirmResetOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    def verify_otp(self):
        code = self.validated_data['otp']
        email = self.validated_data['email']
        
        if ResetPasswordOTP.objects.filter(code=code, email=email).exists():
            try:
                otp = ResetPasswordOTP.objects.get(code=code, email=email)
            except Exception:
                ResetPasswordOTP.objects.filter(code=code, email=email).delete()
                raise serializers.ValidationError(detail='Cannot verify otp. Please try later')
            
            if otp.is_not_expired():
                    
                return {'message': 'success'}
            
            else:
                raise serializers.ValidationError(detail='OTP Expired or Invalid')   
            
            
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=300) 
    
    def reset_password(self):
        try:
            user = User.objects.get(email=self.validated_data['email'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='Error Changing Password')
        
        user.set_password(self.validated_data['password'])
        user.save()
        
        return {'message': 'Password reset complete'}
    

class FireBaseSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=5000)
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=3000) 
    firebase_key = serializers.CharField(max_length=3000, required=False, allow_blank=True)



class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    
    
    def verify_otp(self):
        otp = self.validated_data['otp']
        
        if OTP.objects.filter(code=otp).exists():
            try:
                otp = OTP.objects.get(code=otp)
            except Exception:
                OTP.objects.filter(code=otp).delete()
                raise serializers.ValidationError(detail='Cannot verify otp. Please try later')
            
            if otp.is_not_expired():
                if otp.user.is_active == False:
                    otp.user.is_active=True
                    otp.user.save()
                    
                    #clear all otp for this user after verification
                    all_otps = OTP.objects.filter(user=otp.user)
                    all_otps.delete()
                    
                    serializer = UserSerializer(otp.user)
                    return {'message': 'Verification Complete', 'data':serializer.data}
                else:
                    raise serializers.ValidationError(detail='User with this otp has been verified before.')
            
                
            else:
                raise serializers.ValidationError(detail='OTP expired')
                    
        
        else:
            raise serializers.ValidationError(detail='Invalid OTP')
        
        
class NewOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
     
    def get_new_otp(self):
        try:
            user = User.objects.get(email=self.validated_data['email'], is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='Please confirm that the email is correct and has not been verified')
        
        code = generate_otp(6)
        expiry_date = timezone.now() + timezone.timedelta(minutes=10)
        
        OTP.objects.create(code=code, user=user, expiry_date=expiry_date)
        subject = "NEW OTP FOR SMART PARCEL"
        
        message = f"""Hi, {str(user.first_name).title()}.

    Complete your verification on the smart parcel with the OTP below:

                    {code}        

    Expires in 5 minutes!

    Thank you,
    SmartParcel                
    """
        msg_html = render_to_string('new_otp.html', {
                        'first_name': str(user.first_name).title(),
                        'code':code,
                        'url':url})
        
        email_from = settings.Common.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list, html_message=msg_html)
        
        return {'message': 'Please check your email for OTP.'}
    
    

 