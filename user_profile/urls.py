# urls.py
from django.urls import path
from .views import AvailableDonorsView,UserProfileViewset,UserProfileUpdateView

urlpatterns = [
    path('available/donors/', AvailableDonorsView.as_view(), name='available_donors'),
    path('user_profile/',UserProfileViewset.as_view(),name='user_profile'),
    path('update_profile/',UserProfileUpdateView.as_view(),name='update_profile'),

]
