from django.db import models
from stores.models import Store


class Category(models.Model):
    """Product categories e.g. Electronics, Clothing, Books"""
    name        = models.CharField(max_length=100, unique=True)
    slug        = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Products belong to a vendor's store.
    Only approved vendors can add products.
    """
    STATUS_CHOICES = (
        ('active',   'Active'),
        ('inactive', 'Inactive'),
        ('deleted',  'Deleted'),
    )

    store       = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name        = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField(default=0)
    image       = models.ImageField(upload_to='products/', blank=True, null=True)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} — {self.store.name}"

    def is_in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return f"/products/{self.slug}/"


class ProductImage(models.Model):
    """Extra images for a product (a product can have multiple images)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='product_images/')
    alt     = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"