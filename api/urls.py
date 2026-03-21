from django.urls import path
from .views import DeliveryAddressListCreateView, DeliveryAddressDetailView

urlpatterns = [
    path("addresses/", DeliveryAddressListCreateView.as_view(), name="address-list-create"),
    path("addresses/<int:pk>/", DeliveryAddressDetailView.as_view(), name="address-detail"),
]