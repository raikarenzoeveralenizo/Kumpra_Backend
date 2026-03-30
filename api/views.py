from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from .models import User, DeliveryAddress
from .serializers import RegisterSerializer, UserSerializer, DeliveryAddressSerializer

# --- AUTHENTICATION ---

class RegisterView(generics.CreateAPIView):
    """
    Handles Multi-role Registration (Customer, Seller, Supplier).
    Uses MultiPartParser to handle 'FormData' containing files/images.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    # CRITICAL: Allows the view to accept file uploads (Business Permits, etc.)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user = serializer.save()
        otp_code = user.generate_otp()
        
        # Log to terminal for local testing
        print(f"--- DEBUG: OTP for {user.email} is {otp_code} ---")
        
        subject = "Verify your Kumpra.ph Account"
        message = f"Hello {user.full_name},\n\nYour verification code is: {otp_code}\n\nPlease enter this code to activate your account."
        
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
        email = request.data.get("email")
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
    """Verifies the 6-digit code and activates the account"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

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
    """
    Handles Login. 
    Checks if email is verified AND if Business applications (Sellers/Suppliers) are approved.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user:
            # 1. Check Email Verification
            if not user.is_verified:
                return Response({"error": "Please verify your email first.", "needs_verification": True}, status=status.HTTP_403_FORBIDDEN)

            # 2. Check Business Application Status
            if user.role == 'SELLER':
                if user.store_profile.status != 'APPROVED':
                    return Response({
                        "error": f"Your store application is currently {user.store_profile.status.lower()}.",
                        "status": user.store_profile.status
                    }, status=status.HTTP_403_FORBIDDEN)
            
            elif user.role == 'SUPPLIER':
                if user.supplier_profile.status != 'APPROVED':
                    return Response({
                        "error": f"Your supplier application is currently {user.supplier_profile.status.lower()}.",
                        "status": user.supplier_profile.status
                    }, status=status.HTTP_403_FORBIDDEN)

            # 3. If all checks pass, generate JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# --- ADDRESS VIEWS ---

class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    """Handles GET (all user addresses) and POST (new address)"""
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # SECURITY: Only return addresses belonging to the logged-in user
        return DeliveryAddress.objects.filter(user=self.request.user).order_by('-is_default', '-created_at')

    def perform_create(self, serializer):
        # Tie the address to the account from the token automatically
        serializer.save(user=self.request.user)

class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Handles GET (one), PUT/PATCH (update), and DELETE for a specific address"""
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users can only access/modify their own addresses
        return DeliveryAddress.objects.filter(user=self.request.user)