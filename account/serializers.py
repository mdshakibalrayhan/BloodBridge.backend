from rest_framework import serializers
from .import models
from django.contrib.auth.models import User
from .models import UserAccount
from .constants import GENDER,BLOOD_GROUP
from user_profile.models import UserProfiles
class UserAccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.UserAccount
        fields = '__all__'

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserAccount  

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=GENDER)
    blood_group = serializers.ChoiceField(choices=BLOOD_GROUP)
    image = serializers.ImageField(required=False)
    age = serializers.IntegerField()
    birth_date = serializers.DateField(required=True)
    available_for_donation = serializers.BooleanField()

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password',
            'phone_number', 'address', 'gender', 'blood_group', 'image','age', 'birth_date','available_for_donation',
        ]

    def save(self, **kwargs):

        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        phone_number = self.validated_data['phone_number']
        address = self.validated_data['address']
        gender = self.validated_data['gender']
        blood_group = self.validated_data['blood_group']
        image = self.validated_data.get('image') 
        age = self.validated_data['age']
        birth_date = self.validated_data['birth_date']
        available_for_donation = self.validated_data['available_for_donation']


        if password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords don't match."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email already exists."})

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.is_active = False 
        user.save()

        
        user_account = UserAccount(
            user_account=user,  
            phone_number=phone_number,
            address=address,
            gender=gender,
            blood_group=blood_group,
            birth_date=birth_date
        )
        user_account.save()

        user_profile = UserProfiles(
            user = UserAccount.objects.get(user_account=user),
            age = age,
            image=image,
            is_available=available_for_donation,
        )
        user_profile.save()

        return user

    

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)