import json
from rest_framework import serializers
from .models import DeliveryAddress, User, Store, Supplier

# --- USER SERIALIZER ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "full_name", "email", "contact_number", 
            "gender", "date_of_birth", "role", "is_verified"
        ]
        read_only_fields = ["is_verified"]

# --- REGISTRATION SERIALIZER ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    # These capture Step 2 (Details) and Step 3 (Files) from your Frontend
    store_details = serializers.CharField(write_only=True, required=False)
    company_details = serializers.CharField(write_only=True, required=False)
    
    # Document Uploads for Sellers
    business_permit = serializers.FileField(write_only=True, required=False)
    dti_sec_registration = serializers.FileField(write_only=True, required=False)
    
    # Document Uploads for Suppliers
    registration_cert = serializers.FileField(write_only=True, required=False)
    bir_2303 = serializers.FileField(write_only=True, required=False)
    catalog = serializers.FileField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "full_name", "email", "contact_number", "gender", "date_of_birth", 
            "password", "role", "store_details", "company_details", 
            "business_permit", "dti_sec_registration", "registration_cert", 
            "bir_2303", "catalog"
        ]

    def create(self, validated_data):
        # 1. Extract JSON strings and Files
        store_json = validated_data.pop("store_details", None)
        company_json = validated_data.pop("company_details", None)
        
        # Extract Files
        files = {
            "business_permit": validated_data.pop("business_permit", None),
            "dti_sec_registration": validated_data.pop("dti_sec_registration", None),
            "registration_cert": validated_data.pop("registration_cert", None),
            "bir_2303": validated_data.pop("bir_2303", None),
            "catalog": validated_data.pop("catalog", None),
        }

        # 2. Create the Base User
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
            contact_number=validated_data["contact_number"],
            gender=validated_data.get("gender"),
            date_of_birth=validated_data.get("date_of_birth"),
            role=validated_data.get("role", "CUSTOMER")
        )

        # 3. Handle Store Creation (SELLER)
        if user.role == "SELLER" and store_json:
            store_data = json.loads(store_json)
            Store.objects.create(
                user=user,
                business_permit=files["business_permit"],
                dti_sec_registration=files["dti_sec_registration"],
                **store_data
            )

        # 4. Handle Supplier Creation (SUPPLIER)
        elif user.role == "SUPPLIER" and company_json:
            company_data = json.loads(company_json)
            Supplier.objects.create(
                user=user,
                registration_cert=files["registration_cert"],
                bir_2303=files["bir_2303"],
                catalog=files["catalog"],
                **company_data
            )

        return user

# --- DELIVERY ADDRESS SERIALIZER ---
class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = [
            'id', 'full_name', 'phone', 'region', 'province', 'city', 
            'barangay', 'street_address', 'postal_code', 'label', 
            'is_default', 'lat', 'lng'
        ]
        read_only_fields = ['id']

    def validate_phone(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Phone number is too short.")
        return value