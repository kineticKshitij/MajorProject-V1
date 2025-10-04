from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import api_views

app_name = 'accounts_api'

urlpatterns = [
    # Authentication endpoints
    path('register/', api_views.RegisterAPIView.as_view(), name='register'),
    path('login/', api_views.LoginAPIView.as_view(), name='login'),
    path('logout/', api_views.LogoutAPIView.as_view(), name='logout'),
    
    # Token management
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # User profile
    path('user/', api_views.UserProfileAPIView.as_view(), name='user_profile'),
    path('users/', api_views.UserListAPIView.as_view(), name='user_list'),
    
    # Password management
    path('change-password/', api_views.ChangePasswordAPIView.as_view(), name='change_password'),
    path('forgot-password/', api_views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('verify-otp/', api_views.VerifyOTPAPIView.as_view(), name='verify_otp'),
    path('reset-password/', api_views.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('resend-otp/', api_views.resend_otp, name='resend_otp'),
    
    # API key setup
    path('setup-api-key/', api_views.setup_api_key, name='setup_api_key'),
    path('check-api-key/', api_views.check_api_key, name='check_api_key'),
]
