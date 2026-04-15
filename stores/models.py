from django.db import models
from users.models import User


class Store(models.Model):
    """
    Every vendor has one store.
    Store must be approved by admin before products can be listed.
    """
    vendor      = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    logo        = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    banner      = models.ImageField(upload_to='store_banners/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)   # ← admin must approve
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({'Approved' if self.is_approved else 'Pending'})"

    def total_products(self):
      return self.products.count() 