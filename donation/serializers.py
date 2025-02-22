from rest_framework import serializers
from .models import Donation
from account.models import UserAccount
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['event']
class AllDonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.SerializerMethodField() 
    event_name = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = Donation
        fields = '__all__'  # This will include all fields, including event ID

    def get_donor_name(self, obj):
        return obj.donor.user_account.first_name
    
    def get_event_name(self, obj):
        return obj.event.title  # Assuming your Event model has a 'title' field

