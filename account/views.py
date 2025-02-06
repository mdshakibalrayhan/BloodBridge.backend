from django.shortcuts import render,redirect
from rest_framework import viewsets
from .models import UserAccount
from .serializers import UserAccountSerializer,RegistrationSerializer,UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate,logout,login
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from BloodBridge.settings import SITE_URL
# Create your views here.

class UserAccountViewset(viewsets.ModelViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class UserregistrationAPIView(APIView):
    serializer_class = RegistrationSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print(token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)

            confirm_link = f"{SITE_URL}/account/active/{uid}/{token}"
            email_subject = "Confim Your Email"
            email_body = render_to_string('confirm_email.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject,'',to={user.email})
            email.attach_alternative(email_body,'text/html')
            email.send()
            return Response("check your mail for confirmation.")
            
        return Response(serializer.errors)

def Activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginAPIView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username,password=password)
            if user:
                token,_ = Token.objects.get_or_create(user=user)
                print(user)
                login(request,user)
                print(token)
                print(_)
                return Response({'token':token.key,'user_id':user.id})
            else:
                return Response({'error':'Invalid credential'})
        return Response(serializer.errors)



class UserLogoutView(APIView):
    def get(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            try:
                # Delete the token to log out the user
                request.user.auth_token.delete()
            except Token.DoesNotExist:
                print(request.user)
                return Response({"error": "Token does not exist for the user."})

            # Log out the user session
            logout(request)
            return redirect('login')
        else:
            print('un authenticated')
            # If the user is not authenticated, redirect to login page
            return Response('token does not exist')

'''{
"username":"hasib",
"password":"super1234"
}'''
#https://bloodbridge-backend-31a2.onrender.com/event/update_event/1/