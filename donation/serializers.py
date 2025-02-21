from rest_framework import serializers
from .models import Donation
from account.models import UserAccount
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['event']

class AllDonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.SerializerMethodField() 
    class Meta:
        model = Donation
        fields = '__all__' 

    def get_donor_name(self, obj):
        return obj.donor.user_account.first_name  
