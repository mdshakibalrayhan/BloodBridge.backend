from django.shortcuts import render
from . import serializers
from rest_framework.views import APIView
from rest_framework import viewsets
from .import models
from account.models import UserAccount
from rest_framework.response import Response
from rest_framework import filters
from.constants import BLOOD_GROUP
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

class AddEventSerializerViewset(APIView):
    queryset = models.AllEvent.objects.filter(status='running')
    serializer_class = serializers.AllEventSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            
            data = serializer.save(creator=UserAccount.objects.get(user_account=request.user))
            print(data)
            
        return Response(serializer.errors)

class FilterEvents(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        blood = request.query_params.get("blood")
        
        if blood:

            print(blood)
            blood = blood.upper()
            blood = blood.replace(' ','+')
            print(blood)

            if blood in dict(BLOOD_GROUP): 
                queryset = queryset.filter(blood_group=blood)
                print('filter successfull')
            else:
                
                queryset = queryset.none()
        
        return queryset
    
class AllOnGoingEventsView(APIView):
    def get(self, request):
        events = models.AllEvent.objects.filter(status='running')
        filtered_events = FilterEvents().filter_queryset(request, events, self)
        serializer = serializers.AllEventSerializer(filtered_events, many=True)
        return Response(serializer.data)

class UserSpecificEventsView(APIView):
    def get(self, request):
        user = UserAccount.objects.get(user_account = request.user)
        events = models.AllEvent.objects.filter(creator = user)
        filtered_events = FilterEvents().filter_queryset(request, events, self)
        serializer = serializers.AllEventSerializer(filtered_events, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateEventView(APIView):
    def get(self, request, pk):
        try:
            event = models.AllEvent.objects.get(pk=pk)
            serializer = serializers.AllEventSerializer(event)
            return Response(serializer.data)
        except models.AllEvent.DoesNotExist:
            return Response({'error': 'Event not found'})
        
    def patch(self, request, pk):
        print(pk)
        print(type(pk))
        event = get_object_or_404(models.AllEvent, pk=pk) 
        
        serializer = serializers.AllEventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        return Response(serializer.errors)  
