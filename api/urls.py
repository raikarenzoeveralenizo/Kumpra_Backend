from django.urls import path
from .views import (
    RegisterView, 
    ResendOTPView,
    VerifyEmailView, 
    LoginView, 
    DeliveryAddressListCreateView, 
    DeliveryAddressDetailView
)

urlpatterns = [
    # Auth Endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("login/", LoginView.as_view(), name="login"),
    
    # Address Endpoints
    path("addresses/", DeliveryAddressListCreateView.as_view(), name="address-list-create"),
    path("addresses/<int:pk>/", DeliveryAddressDetailView.as_view(), name="address-detail"),
]