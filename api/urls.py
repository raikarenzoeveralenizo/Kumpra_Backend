from django.urls import path
from .views import (
    RegisterView, 
    VerifyEmailView,  # Import the new view
    LoginView, 
    DeliveryAddressListCreateView, 
    DeliveryAddressDetailView
)

urlpatterns = [
    # Auth Endpoints
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"), # Added this
    path("login/", LoginView.as_view(), name="login"),
    
    # Address Endpoints
    path("addresses/", DeliveryAddressListCreateView.as_view(), name="address-list-create"),
    path("addresses/<int:pk>/", DeliveryAddressDetailView.as_view(), name="address-detail"),
]