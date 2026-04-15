from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model  = OrderItem
    extra  = 0
    readonly_fields = ('product', 'vendor', 'quantity', 'price', 'get_total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display   = ('id', 'customer', 'total_price', 'status', 'created_at')
    list_filter    = ('status',)
    search_fields  = ('customer__username',)
    list_editable  = ('status',)
    inlines        = [OrderItemInline]
    readonly_fields = ('total_price', 'created_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display  = ('order', 'product', 'vendor', 'quantity', 'price', 'status')
    list_filter   = ('status', 'vendor')
    list_editable = ('status',)