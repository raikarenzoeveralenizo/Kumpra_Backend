import random
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

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

class User(AbstractUser):
    # Remove username field, use email as unique identifier
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=11)

    # --- Verification Fields ---
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

class DeliveryAddress(models.Model):
    LABEL_CHOICES = [
        ("Home", "Home"),
        ("Work", "Work"),
        ("Other", "Other"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="delivery_addresses",
        null=True,
        blank=True
    )
    label = models.CharField(max_length=20, choices=LABEL_CHOICES, default="Home")
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    street = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    full_address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-generate full address
        self.full_address = f"{self.street}, {self.region}"
        
        # Ensure only one default address per user
        if self.is_default and self.user:
            DeliveryAddress.objects.filter(
                user=self.user, 
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.label}"