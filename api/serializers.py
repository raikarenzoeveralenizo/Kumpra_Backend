from rest_framework import serializers
from .models import DeliveryAddress, User

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