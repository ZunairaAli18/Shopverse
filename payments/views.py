import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from orders.models import Order, OrderItem
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def create_stripe_session(request, order_id):
    """
    Creates a real Stripe Checkout Session and
    redirects customer to Stripe's hosted payment page.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    # Don't allow paying for already paid orders
    if hasattr(order, 'payment') and order.payment.status == 'completed':
        messages.info(request, 'This order is already paid.')
        return redirect(f'/orders/{order.id}/')

    # Build line items from order items
    line_items = []
    for item in order.items.select_related('product'):
        line_items.append({
            'price_data': {
                'currency':     settings.STRIPE_CURRENCY,
                'unit_amount':  int(item.price * 100),   # in paisa
                'product_data': {
                    'name': item.product.name,
                    'description': f'Sold by {item.vendor.name}',
                },
            },
            'quantity': item.quantity,
        })

    # Create Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items           = line_items,
        mode                 = 'payment',
        
        # Where to redirect after payment
        success_url = request.build_absolute_uri(
            f'/payments/success/{order.id}/'
        ) + '?session_id={CHECKOUT_SESSION_ID}',
        
        cancel_url = request.build_absolute_uri(
            f'/payments/cancelled/{order.id}/'
        ),

        # Attach order id to session metadata
        metadata = {
            'order_id': order.id,
            'customer': request.user.username,
        }
    )

    # Save pending payment record with session id
    Payment.objects.update_or_create(
        order  = order,
        defaults = {
            'method':           'stripe',
            'status':           'pending',
            'amount':           order.total_price,
            'stripe_charge_id': session.id,   # store session id for verification
        }
    )

    # Redirect to Stripe's real hosted payment page
    return redirect(session.url, code=303)


@login_required
def payment_success(request, order_id):
    """
    Stripe redirects here after successful payment.
    Verify the session and confirm the order.
    """
    order      = get_object_or_404(Order, id=order_id, customer=request.user)
    session_id = request.GET.get('session_id')

    if not session_id:
        messages.error(request, 'Invalid payment session.')
        return redirect(f'/orders/{order.id}/')

    try:
        # Verify payment with Stripe
        session = stripe.checkout.Session.retrieve(session_id)

        if session.payment_status == 'paid':
            # ─── Update Payment record ─────────────────
            payment = order.payment
            payment.status           = 'completed'
            payment.stripe_charge_id = session.payment_intent
            payment.save()

            # ─── Confirm the order ──────────────────────
            order.status = 'confirmed'
            order.save()

            # ─── Confirm all order items ────────────────
            order.items.all().update(status='confirmed')

            messages.success(request, f'Payment successful! Order #{order.id} confirmed.')

        else:
            messages.error(request, 'Payment not completed. Please try again.')
            return redirect(f'/payments/stripe/{order.id}/')

    except stripe.error.StripeError as e:
        messages.error(request, f'Payment verification failed: {str(e)}')
        return redirect(f'/orders/{order.id}/')

    return render(request, 'payments/payment_success.html', {
        'order':   order,
        'payment': order.payment,
    })


@login_required
def payment_cancelled(request, order_id):
    """
    Stripe redirects here if customer cancels payment.
    Order stays pending so they can try again.
    """
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    messages.warning(request, 'Payment cancelled. Your order is still saved — try again.')
    return render(request, 'payments/payment_cancelled.html', {'order': order})