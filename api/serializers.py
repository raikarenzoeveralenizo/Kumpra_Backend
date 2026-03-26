from rest_framework import serializers
from .models import DeliveryAddress, User

# --- USER SERIALIZER ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "email",
            "contact_number",
            "gender",
            "date_of_birth",
            "is_verified",
        ]
        read_only_fields = ["is_verified"]

# --- REGISTRATION SERIALIZER ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "contact_number",
            "gender",
            "date_of_birth",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
            contact_number=validated_data["contact_number"],
            gender=validated_data.get("gender"),
            date_of_birth=validated_data.get("date_of_birth"),
        )
        return user

# --- DELIVERY ADDRESS SERIALIZER ---
class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = [
            'id', 
            'full_name', 
            'phone', 
            'region', 
            'province', 
            'city', 
            'barangay', 
            'street_address', 
            'postal_code', 
            'label', 
            'is_default', 
            'lat', 
            'lng'
        ]
        read_only_fields = ['id']

    def validate_phone(self, value):
        """Optional: Add custom validation for PH phone numbers."""
        if len(value) < 10:
            raise serializers.ValidationError("Phone number is too short.")
        return value