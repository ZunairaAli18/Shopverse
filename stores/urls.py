from django.urls import path
from . import views

urlpatterns = [
    path('create/',    views.create_store, name='create_store'),
    path('dashboard/', views.dashboard,    name='vendor_dashboard'),
    path('edit/',      views.edit_store,   name='edit_store'),
]