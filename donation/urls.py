from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
#router.register('list', views.AllEventSerializerViewset) 

urlpatterns = [
    path('', include(router.urls)),
    path('donate_blood/',views.DonationSerializerViewset.as_view(),name='donate_blood'),
    path('donation_history/',views.DonationHistory.as_view(),name='donation_history'),
    path('requests/<int:pk>/',views.RequestOfSpecificEvent.as_view(),name='request'),
]