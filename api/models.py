import random
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

# --- USER MANAGER ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        
        # Default new users to unverified
        extra_fields.setdefault("is_verified", False)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # Superusers should be verified automatically
        extra_fields.setdefault("is_verified", True)
        
        return self.create_user(email, password, **extra_fields)

# --- CUSTOM USER MODEL ---
class User(AbstractUser):
    # Remove username field, use email as unique identifier
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=11)

    # Verification Fields
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "contact_number"]

    objects = UserManager()

    def __str__(self):
        return self.email

    def generate_otp(self):
        """Generates a random 6-digit code and saves it to the user."""
        code = str(random.randint(100000, 999999))
        self.otp = code
        self.save()
        return code

# --- DELIVERY ADDRESS MODEL ---
class DeliveryAddress(models.Model):
    # Links to the User model above
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="addresses"
    )
    
    # Recipient Info
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    
    # Philippine Address Hierarchy (matching your React Modal)
    region = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    barangay = models.CharField(max_length=100)
    
    # Specific Location Details
    street_address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    label = models.CharField(max_length=20, default="Home") # e.g., "Home", "Work"
    is_default = models.BooleanField(default=False)
    
    # Coordinates for the Leaflet Map View
    lat = models.DecimalField(max_digits=12, decimal_places=9)
    lng = models.DecimalField(max_digits=12, decimal_places=9)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Delivery Address"
        verbose_name_plural = "Delivery Addresses"

    def save(self, *args, **kwargs):
        # If this address is set as default, set all other user addresses to False
        if self.is_default:
            DeliveryAddress.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} - {self.full_name} ({self.city})"