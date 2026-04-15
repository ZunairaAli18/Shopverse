from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model. Extends Django's built-in User
    and adds a role field to distinguish customers, vendors, and admins.
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('vendor',   'Vendor'),
        ('admin',    'Admin'),
    )

    role  = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def is_vendor(self):
        return self.role == 'vendor'

    def is_customer(self):
        return self.role == 'customer'

    def __str__(self):
        return f"{self.username} ({self.role})"