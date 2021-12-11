from django.urls import path
from .views import *
#from rest_framework.authtoken.views import obtain_auth_token
from .serializers import LoginToken

urlpatterns = [
    path('login/', LoginToken.as_view(), name='login'),
    path('register/', Registration, name='register'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('dashboard/<int:pk>/', Dashboard.as_view(), name='dashboard_detail'),
    path('token/', IsTokenValid.as_view(), name='is_token_valid'),
    path('version/', Version, name='version'),
    path('logout/', Logout, name='logout'),
]