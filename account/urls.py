from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import UserAccountViewset,UserregistrationAPIView,Activate,UserLoginAPIView,UserLogoutView
router = DefaultRouter()

router.register('list',UserAccountViewset)
urlpatterns = [
    path('',include(router.urls)),
    path('register/',UserregistrationAPIView.as_view(),name='register'),
    path('login/',UserLoginAPIView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('active/<uid64>/<token>/',Activate,name='activate'),
]
