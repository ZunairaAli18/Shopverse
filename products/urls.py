from django.urls import path
from . import views

urlpatterns = [
    # Vendor product management
    path('add/',                views.add_product,     name='add_product'),
    path('manage/',             views.manage_products, name='manage_products'),
    path('edit/<slug:slug>/',   views.edit_product,    name='edit_product'),
    path('delete/<slug:slug>/', views.delete_product,  name='delete_product'),

    # Public pages
    path('',                    views.product_list,    name='product_list'),
    path('<slug:slug>/',        views.product_detail,  name='product_detail'),
]