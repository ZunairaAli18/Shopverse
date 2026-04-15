from django.urls import path
from . import views

urlpatterns = [
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/vendor/',   views.register_vendor,   name='register_vendor'),
    path('login/',             views.login_view,         name='login'),
    path('logout/',            views.logout_view,        name='logout'),
]