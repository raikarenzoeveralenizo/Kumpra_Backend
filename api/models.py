from django.db import models
from django.contrib.auth.models import User


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
        self.full_address = f"{self.street}, {self.region}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.label}"