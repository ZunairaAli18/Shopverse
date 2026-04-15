from django.urls import path
from . import views

urlpatterns = [
    path('stripe/<int:order_id>/',      views.create_stripe_session, name='stripe_payment'),
    path('success/<int:order_id>/',     views.payment_success,       name='payment_success'),
    path('cancelled/<int:order_id>/',   views.payment_cancelled,     name='payment_cancelled'),
]