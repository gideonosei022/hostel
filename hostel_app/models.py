from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'House Owner / Agent'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='owner')

    def __str__(self):
        return f"{self.username} ({self.role})"


# Property Listings
class Property(models.Model):
    PROPERTY_TYPE_CHOICES = (
        ('room', 'Room'),
        ('house', 'Entire House'),
    )

    REGION_CHOICES = [
        ('greater_accra', 'Greater Accra'),
        ('ashanti', 'Ashanti'),
        ('western', 'Western'),
        ('eastern', 'Eastern'),
        ('central', 'Central'),
        ('volta', 'Volta'),
        ('northern', 'Northern'),
        ('upper_east', 'Upper East'),
        ('upper_west', 'Upper West'),
        ('bono', 'Bono'),
        ('bono_east', 'Bono East'),
        ('ahafo', 'Ahafo'),
        ('western_north', 'Western North'),
        ('savannah', 'Savannah'),
        ('north_east', 'North East'),
        ('oti', 'Oti'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties'
    )

    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    region = models.CharField(max_length=20, choices=REGION_CHOICES)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPE_CHOICES)

    description = models.TextField()
    is_available = models.BooleanField(default=True)

    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.location}"


# Property Images
class PropertyImage(models.Model):
    property = models.ForeignKey('hostel_app.Property', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


# Favorites (for Tenants)
class Favorite(models.Model):
    tenant = models.ForeignKey('hostel_app.User', on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey('hostel_app.Property', on_delete=models.CASCADE, related_name='favorited_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tenant', 'property')

    def __str__(self):
        return f"{self.tenant.username} saved {self.property.title}"


# Messages between Users
class Message(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message for {self.property.title} from {self.sender_name}"
