from django.urls import path
from . import views

urlpatterns = [
    # Customer
    path('checkout/',              views.checkout,                 name='checkout'),
    path('',                       views.order_list,               name='order_list'),
    path('<int:order_id>/',        views.order_detail,             name='order_detail'),
    path('<int:order_id>/cancel/', views.cancel_order,             name='cancel_order'),

    # Vendor
    path('vendor/',                        views.vendor_orders,             name='vendor_orders'),
    path('vendor/update/<int:item_id>/',   views.vendor_update_order_item,  name='vendor_update_item'),
]