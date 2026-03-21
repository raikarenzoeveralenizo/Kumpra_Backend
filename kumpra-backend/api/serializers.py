from rest_framework import serializers
from .models import DeliveryAddress


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = [
            "id",
            "user",
            "label",
            "full_name",
            "phone",
            "street",
            "region",
            "full_address",
            "latitude",
            "longitude",
            "is_default",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "full_address", "created_at", "updated_at"]

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain digits only.")
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be exactly 11 digits.")
        return value