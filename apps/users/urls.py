from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from apps.users.views import UserAPIViewsSet, UserRegisterAPI, UserAPI

router = DefaultRouter()

router.register('users/', UserAPIViewsSet, 'api_users')

urlpatterns = [
    path('', UserAPI.as_view(), name='api_users'),
    path('login/', TokenObtainPairView.as_view(), name='api_users_login'),
    path('refresh/', TokenRefreshView.as_view(), name='api_users_refresh'),
    path('register/', UserRegisterAPI.as_view(), name="api_users_register"),
    
]

