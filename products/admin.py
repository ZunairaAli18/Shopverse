from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}   # ← auto-fills slug from name


class ProductImageInline(admin.TabularInline):
    model  = ProductImage
    extra  = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ('name', 'store', 'category', 'price', 'stock', 'status')
    list_filter   = ('status', 'category')
    search_fields = ('name', 'store__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines       = [ProductImageInline]