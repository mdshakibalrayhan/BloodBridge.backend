from rest_framework import serializers
from .models import AllEvent

class AllEventSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(many=False)
    class Meta:
        model = AllEvent
        fields = ['id','creator','title','description','blood_group','location','time','status']