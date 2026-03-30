import random
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

# --- DYNAMIC UPLOAD PATHS ---

def supplier_doc_path(instance, filename):
    # Organizes files into media/suppliers/CompanyName/filename
    return f"suppliers/{instance.company_name.replace(' ', '_')}/{filename}"

def seller_doc_path(instance, filename):
    # Organizes files into media/sellers/StoreName/filename
    return f"sellers/{instance.store_name.replace(' ', '_')}/{filename}"


# --- USER MANAGER ---

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        
        extra_fields.setdefault("is_verified", False)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        # Superusers are Admins by default
        extra_fields.setdefault("role", "ADMIN")
        
        return self.create_user(email, password, **extra_fields)


# --- CUSTOM USER MODEL ---

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=11)

    # Multi-Role Logic
    ROLE_CHOICES = [
        ("CUSTOMER", "Customer"),
        ("SELLER", "Store Seller"),
        ("SUPPLIER", "Supplier"),
        ("ADMIN", "Admin"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="CUSTOMER")

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "contact_number"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    def generate_otp(self):
        code = str(random.randint(100000, 999999))
        self.otp = code
        self.save()
        return code


# --- STORE / SELLER MODEL ---

class Store(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="store_profile")
    store_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # Business Location
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    
    # Verification Documents
    business_permit = models.FileField(upload_to=seller_doc_path)
    dti_sec_registration = models.FileField(upload_to=seller_doc_path)
    
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.store_name


# --- SUPPLIER MODEL ---

class Supplier(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="supplier_profile")
    company_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100) 
    product_category = models.CharField(max_length=100)
    
    # Logistics Info
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    min_order_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    delivery_areas = models.TextField() 

    # Verification Documents
    registration_cert = models.FileField(upload_to=supplier_doc_path)
    bir_2303 = models.FileField(upload_to=supplier_doc_path)
    catalog = models.FileField(upload_to=supplier_doc_path, blank=True, null=True)

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# --- DELIVERY ADDRESS MODEL ---

class DeliveryAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="addresses"
    )
    
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    label = models.CharField(max_length=20, default="Home")
    is_default = models.BooleanField(default=False)
    
    lat = models.DecimalField(max_digits=12, decimal_places=9)
    lng = models.DecimalField(max_digits=12, decimal_places=9)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Delivery Address"
        verbose_name_plural = "Delivery Addresses"

    def save(self, *args, **kwargs):
        if self.is_default:
            DeliveryAddress.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} - {self.full_name} ({self.city})"