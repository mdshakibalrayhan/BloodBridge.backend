from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.utils.timezone import now
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from . import serializers
from .models import Donation
from account.models import UserAccount
from user_profile.models import UserProfiles

class DonationSerializerViewset(APIView):
    """
    Handles listing and creating donation requests.
    """
    
    def get(self, request):
        donations = Donation.objects.all()
        serializer = serializers.AllDonationSerializer(donations, many=True)
        print('userID:', request.user.id)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = serializers.DonationSerializer(data=request.data)  # Make sure to use correct serializer

        if serializer.is_valid():
            event = serializer.validated_data['event']
            user = get_object_or_404(UserAccount, user_account=request.user) 
            donated_blood = user.blood_group

            if event.blood_group != donated_blood:
                return Response(
                    {"error": "Your blood group does not match the event's required blood group."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            donation = serializer.save(
                donor=user, 
                donation_date=now(), 
                donated_blood_group=donated_blood
            )
            return Response(
                {"message": "Donation request submitted successfully", "donation": serializers.AllDonationSerializer(donation).data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DonationHistory(APIView):
    """
    Retrieves donation history for an authenticated user.
    """
    
    def get(self, request):
        user = get_object_or_404(UserAccount, user_account=request.user)
        donations = Donation.objects.filter(donor=user)
        serializer = serializers.AllDonationSerializer(donations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestOfSpecificEvent(APIView):
    """
    Retrieves all donation requests related to a specific event.
    """
    
    def get(self, request, pk):
        event_requests = Donation.objects.filter(event__id=pk)
        serializer = serializers.AllDonationSerializer(event_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateRequest(APIView):
    """
    Handles updating the status of a donation request.
    """
    
    def get(self, request, pk):
        request_instance = get_object_or_404(Donation, pk=pk)
        serializer = serializers.AllDonationSerializer(request_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        request_instance = get_object_or_404(Donation, pk=pk)

        # Update request status
        request_instance.request_status = True  
        
        # Send email notification
        email_subject = "Your Donation Request Has Been Accepted"
        email_body = render_to_string('admin_email.html', {
            'user': request_instance.donor,
            'event': request_instance.event
        })
        
        email = EmailMultiAlternatives(email_subject, '', to=[request_instance.donor.user_account.email])
        email.attach_alternative(email_body, "text/html")
        email.send()

        # Update the user's last donation date
        user_profile = get_object_or_404(UserProfiles, user=request_instance.donor)
        user_profile.last_donation_date = request_instance.event.time
        user_profile.save()

        request_instance.save()
        return Response({"message": "Request accepted"}, status=status.HTTP_200_OK)
