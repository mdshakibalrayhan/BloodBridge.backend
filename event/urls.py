from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
#router.register('list', views.AllEventSerializerViewset) 

urlpatterns = [
    path('', include(router.urls)),
    path('all_events/',views.AllOnGoingEventsView.as_view(),name='all_events'),
    path('add_event/',views.AddEventSerializerViewset.as_view(),name='add_event'),
    path('update_event/<int:pk>/',views.UpdateEventView.as_view(),name='update_event'),
]