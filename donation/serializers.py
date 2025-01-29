from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['event']

class AllDonationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = Donation
        fields = '__all__'