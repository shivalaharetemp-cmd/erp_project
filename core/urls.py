from django.urls import path
from rest_framework.authtoken import views as drf_token_views
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.UserProfileView.as_view(), name='user-profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('token/', drf_token_views.obtain_auth_token, name='api-token-auth'),
]
