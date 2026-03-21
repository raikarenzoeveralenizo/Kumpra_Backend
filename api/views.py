from rest_framework import generics
from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer


class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    queryset = DeliveryAddress.objects.all().order_by("-id")
    serializer_class = DeliveryAddressSerializer


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer