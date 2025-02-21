from django.shortcuts import render
from . import serializers
from rest_framework.views import APIView
from rest_framework import viewsets
from .import models
from account.models import UserAccount
from rest_framework.response import Response
from django.utils.timezone import now
from user_profile.models import UserProfiles
from rest_framework.exceptions import ValidationError
from .models import Donation
# Create your views here.

class DonationSerializerViewset(APIView):
    #queryset = models.Donation.objects.all()
    def get(self, request):
        donations = Donation.objects.all()
        serializer = serializers.AllDonationSerializer(donations,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            event = serializer.validated_data['event']
            user = UserAccount.objects.get(user_account=request.user) 
            donated_blood = user.blood_group
            if event.blood_group != donated_blood:
                raise ValidationError(
                    {"donated_blood_group": "Your blood group does not match the event's required blood group."}
                )
            else:
                data = serializer.save(donor=UserAccount.objects.get(user_account=request.user),donation_date=now(),donated_blood_group=donated_blood)
                print(data)
            
        return Response(serializer.errors)
    

class DonationHistory(APIView):
    def get(self, request):
        print(request.user)
        user = UserAccount.objects.get(user_account = request.user)
        events = models.Donation.objects.filter(donor=user)
        serializer = serializers.AllDonationSerializer(events, many=True)
        return Response(serializer.data)
    
class  RequestOfSpecificEvent(APIView):
    def get(self, request,pk):
        print(request.user)
        Requests = models.Donation.objects.filter(pk=pk)
        serializer = serializers.AllDonationSerializer(Requests, many=True)
        return Response(serializer.data)
