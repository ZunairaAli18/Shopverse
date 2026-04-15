from django.db import models
from users.models import User
from products.models import Product
from stores.models import Store


class Order(models.Model):
    """
    One order per checkout by a customer.
    Contains items from multiple vendors.
    """
    STATUS_CHOICES = (
        ('pending',    'Pending'),
        ('confirmed',  'Confirmed'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    )

    customer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    # Shipping details
    full_name   = models.CharField(max_length=100)
    phone       = models.CharField(max_length=15)
    address     = models.TextField()
    city        = models.CharField(max_length=50)
    
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

    def get_vendor_items(self, store):
        """Get all items in this order that belong to a specific vendor"""
        return self.items.filter(vendor=store)

    def get_vendor_total(self, store):
        """Total price for a specific vendor's items"""
        items = self.get_vendor_items(store)
        return sum(item.get_total_price() for item in items)


class OrderItem(models.Model):
    """
    Each line item in an order.
    Linked to both the order AND the vendor — this is what enables order splitting.
    """
    STATUS_CHOICES = (
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped',   'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    order    = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor   = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price    = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order
    status   = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

    def get_total_price(self):
        return self.price * self.quantity