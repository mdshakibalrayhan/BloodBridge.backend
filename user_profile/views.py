from django.shortcuts import render
from .models import UserProfiles
from . import serilizers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from account.models import UserAccount
from django.contrib.auth.models import User
# Create your views here.
# '''
class FilterDonors(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        id = request.query_params.get("id")
        
        if id:
            # Capitalize the blood group to match the format (e.g., 'b+' -> 'B+')
            print(id)
            queryset = queryset.filter(id=id)
            print('filter successfull')
        
        
        return queryset

class AvailableDonorsView(APIView):
    def get(self, request):
        donors = UserProfiles.objects.filter(is_available=True)
        serializer = serilizers.UserProfilesSerializer(donors, many=True, context={'request': request})
        return Response(serializer.data)
    
class UserProfileViewset(APIView):
    def get(self, request):
        user = UserProfiles.objects.get(user=UserAccount.objects.get(user_account=request.user))
        serializer = serilizers.UserProfilesSerializer(user)
        return Response(serializer.data)
    

class UserProfileUpdateView(APIView):
    def get_object(self, request):
        user = UserAccount.objects.get(user_account= request.user)
        user_profile = UserProfiles.objects.get(user=user)
        return user_profile
    
    def patch(self, request, *args, **kwargs):
        """Handle patch request to update user profile"""
        user_profile = self.get_object(request) 
        user_account = user_profile.user
        user = user_account.user_account
        data = request.data

        for x in data:
            
            if x !='user' and x !='age' and x != 'is_available' and x!='last_donation_date':
                if x != 'first_name' and   x != 'last_name':
                    setattr(user_account,x,data[x])
                    user_account.save()
                    print('user_account save kortaci',x)
                else:
                    setattr(user,x,data[x])
                    user.save()
                    print('user er data save kortesi')

        serializer = serilizers.UserProfilesSerializer(user_profile, data=request.data, partial=True)
        
        if serializer.is_valid(): 
            serializer.save() 
             # Save the updated data
            return Response(serializer.data)  # Return updated data in the response
        return Response(serializer.errors, status=400)