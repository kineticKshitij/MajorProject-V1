from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import PasswordResetOTP
from .email_utils import send_otp_email, send_password_reset_success_email
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    UserUpdateSerializer, ChangePasswordSerializer,
    TokenObtainPairResponseSerializer,
    ForgotPasswordSerializer, VerifyOTPSerializer, ResetPasswordSerializer
)

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    """
    API endpoint for user registration
    POST /api/auth/register/
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """
    API endpoint for user login
    POST /api/auth/login/
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            'message': f'Welcome back, {user.get_full_name() or user.username}!'
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    API endpoint for user logout
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for current user profile
    GET /api/auth/user/
    PUT/PATCH /api/auth/user/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordAPIView(APIView):
    """
    API endpoint for changing password
    POST /api/auth/change-password/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Set new password
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password updated successfully'
        }, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    """
    API endpoint for listing users (admin only)
    GET /api/auth/users/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_api_key(request):
    """
    API endpoint for setting up Gemini API key
    POST /api/auth/setup-api-key/
    """
    api_key = request.data.get('gemini_api_key', '').strip()
    
    if not api_key:
        return Response({
            'error': 'API key is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    request.user.gemini_api_key = api_key
    request.user.save()
    
    return Response({
        'message': 'API key updated successfully',
        'has_api_key': request.user.has_gemini_api_key()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_api_key(request):
    """
    API endpoint for checking if user has API key configured
    GET /api/auth/check-api-key/
    """
    return Response({
        'has_api_key': request.user.has_gemini_api_key(),
        'api_key': request.user.gemini_api_key if request.user.has_gemini_api_key() else None
    })


class ForgotPasswordAPIView(APIView):
    """
    API endpoint for initiating password reset (send OTP to email)
    POST /api/auth/forgot-password/
    """
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Invalidate all previous OTPs for this user
        PasswordResetOTP.objects.filter(user=user, is_used=False).update(is_used=True)
        
        # Generate new OTP
        otp_code = PasswordResetOTP.generate_otp()
        
        # Get client IP address
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or \
                     request.META.get('REMOTE_ADDR')
        
        # Create OTP record
        otp = PasswordResetOTP.objects.create(
            user=user,
            otp_code=otp_code,
            ip_address=ip_address
        )
        
        # Send OTP email
        email_sent = send_otp_email(user, otp_code)
        
        if email_sent:
            return Response({
                'message': 'OTP has been sent to your email address',
                'email': email,
                'expires_in': '10 minutes'
            }, status=status.HTTP_200_OK)
        else:
            # Delete the OTP if email failed
            otp.delete()
            return Response({
                'error': 'Failed to send OTP email. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPAPIView(APIView):
    """
    API endpoint for verifying OTP (without resetting password)
    POST /api/auth/verify-otp/
    """
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response({
            'message': 'OTP verified successfully',
            'valid': True
        }, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    """
    API endpoint for resetting password with OTP
    POST /api/auth/reset-password/
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        
        # Mark OTP as used
        otp.is_used = True
        otp.save()
        
        # Reset password
        user.set_password(new_password)
        user.save()
        
        # Send confirmation email
        send_password_reset_success_email(user)
        
        # Invalidate all other OTPs for this user
        PasswordResetOTP.objects.filter(user=user, is_used=False).update(is_used=True)
        
        return Response({
            'message': 'Password reset successful. You can now log in with your new password.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    """
    API endpoint for resending OTP
    POST /api/auth/resend-otp/
    """
    email = request.data.get('email')
    
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({
            'error': 'No user found with this email address'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Check if user has requested OTP too many times recently (rate limiting)
    recent_otps = PasswordResetOTP.objects.filter(
        user=user,
        created_at__gte=timezone.now() - timezone.timedelta(minutes=5)
    ).count()
    
    if recent_otps >= 3:
        return Response({
            'error': 'Too many OTP requests. Please try again after 5 minutes.'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    # Invalidate previous OTPs
    PasswordResetOTP.objects.filter(user=user, is_used=False).update(is_used=True)
    
    # Generate new OTP
    otp_code = PasswordResetOTP.generate_otp()
    
    # Get client IP address
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or \
                 request.META.get('REMOTE_ADDR')
    
    # Create OTP record
    otp = PasswordResetOTP.objects.create(
        user=user,
        otp_code=otp_code,
        ip_address=ip_address
    )
    
    # Send OTP email
    email_sent = send_otp_email(user, otp_code)
    
    if email_sent:
        return Response({
            'message': 'New OTP has been sent to your email address',
            'email': email,
            'expires_in': '10 minutes'
        }, status=status.HTTP_200_OK)
    else:
        otp.delete()
        return Response({
            'error': 'Failed to send OTP email. Please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
