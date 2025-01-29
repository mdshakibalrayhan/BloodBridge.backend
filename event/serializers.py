from rest_framework import serializers
from .models import AllEvent

class AllEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllEvent
        fields = ['id','title','description','blood_group','location','time','status']