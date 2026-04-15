from django.db import models
from orders.models import Order


class Payment(models.Model):
    """
    Tracks payment for each order.
    One payment per order.
    """
    METHOD_CHOICES = (
        ('stripe', 'Stripe'),
        ('cod',    'Cash on Delivery'),
    )

    STATUS_CHOICES = (
        ('pending',   'Pending'),
        ('completed', 'Completed'),
        ('failed',    'Failed'),
        ('refunded',  'Refunded'),
    )

    order          = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method         = models.CharField(max_length=10, choices=METHOD_CHOICES)
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=100, blank=True)  # Stripe transaction ID
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order #{self.order.id} — {self.method} ({self.status})"