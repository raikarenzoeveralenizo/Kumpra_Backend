from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken # Added for actual login session
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User, DeliveryAddress
from .serializers import RegisterSerializer, UserSerializer, DeliveryAddressSerializer

# --- AUTHENTICATION ---

class RegisterView(generics.CreateAPIView):
    """Handles User Registration and sends OTP email"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        otp_code = user.generate_otp()
        
        # Log to terminal for local debugging
        print(f"--- DEBUG: OTP for {user.email} is {otp_code} ---")
        
        subject = "Verify your Kumpra.ph Account"
        message = f"Hello {user.full_name},\n\nYour verification code is: {otp_code}\n\nPlease enter this code in the app to activate your account."
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
        except Exception as e:
            print(f"Email failed to send: {e}")

class ResendOTPView(APIView):
    """Endpoint to resend OTP if the user didn't receive it"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email, is_verified=False)
            otp_code = user.generate_otp()
            
            send_mail(
                "Your New Kumpra.ph Verification Code",
                f"Your new code is: {otp_code}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False
            )
            return Response({"message": "New OTP sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found or already verified."}, status=status.HTTP_404_NOT_FOUND)

class VerifyEmailView(APIView):
    """Endpoint to verify the 6-digit OTP code"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if user.otp == otp:
                user.is_verified = True
                user.otp = None
                user.save()
                return Response({
                    "message": "Email verified successfully.",
                    "is_verified": True
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    """Handles User Login with JWT Token generation"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user:
            if not user.is_verified:
                return Response(
                    {"error": "Please verify your email before logging in.", "needs_verification": True}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Generate JWT Tokens so the user stays logged in on Next.js
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "message": "Login successful"
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)

# --- DELIVERY ADDRESSES ---

class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)