from django.db import models
from users.models import User
from products.models import Product


class Cart(models.Model):
    """
    One cart per user.
    Cart can have items from multiple vendors at the same time.
    """
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total_price(self):
        """Total price of all items in cart"""
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        """Total number of items in cart"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Each item in the cart.
    Linked to a product and a cart.
    """
    cart       = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity   = models.PositiveIntegerField(default=1)
    added_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """Price of this item × quantity"""
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('cart', 'product')   # same product can't be added twice