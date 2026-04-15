import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.models import Cart
from payments.models import Payment
from stores.decorators import vendor_required

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('/cart/')

    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('/cart/')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():

            # ─── Create Order ──────────────────────────────
            order             = form.save(commit=False)
            order.customer    = request.user
            order.total_price = cart.get_total_price()
            order.status      = 'pending'
            order.save()

            # ─── Split cart into OrderItems ────────────────
            for cart_item in cart.items.select_related('product', 'product__store'):
                OrderItem.objects.create(
                    order    = order,
                    product  = cart_item.product,
                    vendor   = cart_item.product.store,
                    quantity = cart_item.quantity,
                    price    = cart_item.product.price,
                )
                product        = cart_item.product
                product.stock -= cart_item.quantity
                product.save()

            # ─── Clear cart ────────────────────────────────
            cart.items.all().delete()

            # ─── Handle Payment Method ─────────────────────
            payment_method = form.cleaned_data['payment_method']

            if payment_method == 'cod':
                # Cash on Delivery — create pending payment
                Payment.objects.create(
                    order  = order,
                    method = 'cod',
                    status = 'pending',
                    amount = order.total_price,
                )
                order.status = 'confirmed'
                order.save()
                messages.success(request, f'Order #{order.id} placed! Pay on delivery.')
                return redirect(f'/orders/{order.id}/')

            elif payment_method == 'stripe':
                # Redirect to Stripe payment page
                return redirect(f'/payments/stripe/{order.id}/')

        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CheckoutForm(initial={
            'full_name': request.user.get_full_name() or request.user.username,
            'phone':     request.user.phone,
        })

    cart_items = cart.items.select_related('product', 'product__store').all()

    return render(request, 'orders/checkout.html', {
        'form':       form,
        'cart':       cart,
        'cart_items': cart_items,
    })


@login_required
def order_detail(request, order_id):
    """Customer views a single order"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.items.select_related('product', 'vendor').all()

    # Group items by vendor
    vendors = {}
    for item in items:
        if item.vendor not in vendors:
            vendors[item.vendor] = []
        vendors[item.vendor].append(item)

    return render(request, 'orders/order_detail.html', {
        'order':   order,
        'vendors': vendors,
    })


@login_required
def order_list(request):
    """Customer views all their orders"""
    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-created_at')

    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    """Customer cancels a pending order"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    if order.status not in ['pending', 'confirmed']:
        messages.error(request, 'Orders can only be cancelled before shipping.')
        return redirect(f'/orders/{order.id}/')

    if request.method == 'POST':
        # Restore stock
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
            item.status = 'cancelled'
            item.save()

        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} cancelled.')
        return redirect('/orders/')

    return render(request, 'orders/cancel_order.html', {'order': order})


# ─── Vendor Views ──────────────────────────────────────

@vendor_required
def vendor_orders(request):
    """Vendor sees only their own order items"""
    order_items = OrderItem.objects.filter(
        vendor=request.user.store
    ).select_related('order', 'product', 'order__customer').order_by('-order__created_at')

    return render(request, 'orders/vendor_orders.html', {'order_items': order_items})


@vendor_required
def vendor_update_order_item(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, vendor=request.user.store)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']

        if new_status in valid_statuses:
            item.status = new_status
            item.save()

            # ─── Auto-update the parent Order status ──────
            order = item.order
            all_items = order.items.all()

            # Check what statuses all items have
            statuses = set(all_items.values_list('status', flat=True))

            if all(s == 'delivered' for s in statuses):
                order.status = 'delivered'       # all items delivered

            elif all(s == 'cancelled' for s in statuses):
                order.status = 'cancelled'       # all items cancelled

            elif any(s == 'shipped' for s in statuses):
                order.status = 'shipped'         # at least one shipped

            elif all(s in ['confirmed', 'delivered'] for s in statuses):
                order.status = 'confirmed'       # all confirmed or delivered

            else:
                order.status = 'pending'         # still has pending items

            order.save()
            # ──────────────────────────────────────────────

            messages.success(request, f'Status updated to "{new_status}".')
        else:
            messages.error(request, 'Invalid status.')

    return redirect('/orders/vendor/')