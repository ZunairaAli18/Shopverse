from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product


def get_or_create_cart(user):
    """Helper — gets existing cart or creates one for the user"""
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def cart_detail(request):
    """Show the cart page with items grouped by vendor"""
    cart = get_or_create_cart(request.user)
    items = cart.items.select_related('product', 'product__store').all()

    # Group items by vendor/store
    vendors = {}
    for item in items:
        store = item.product.store
        if store not in vendors:
            vendors[store] = []
        vendors[store].append(item)

    context = {
        'cart':         cart,
        'vendors':      vendors,
        'total_price':  cart.get_total_price(),
        'total_items':  cart.get_total_items(),
    }
    return render(request, 'cart/cart_detail.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add a product to cart or increase quantity if already exists"""
    product = get_object_or_404(Product, id=product_id, status='active')

    # Vendors cannot buy their own products
    if request.user.role == 'vendor':
        messages.error(request, 'Vendors cannot add products to cart.')
        return redirect(f'/products/{product.slug}/')

    # Check stock
    if not product.is_in_stock():
        messages.error(request, 'Sorry, this product is out of stock.')
        return redirect(f'/products/{product.slug}/')

    cart = get_or_create_cart(request.user)

    # Get quantity from form (default 1)
    quantity = int(request.POST.get('quantity', 1))

    # If item already in cart, increase quantity
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        # Item already exists — increase quantity
        new_quantity = cart_item.quantity + quantity
        # Don't exceed stock
        if new_quantity > product.stock:
            messages.warning(request, f'Only {product.stock} items available.')
            cart_item.quantity = product.stock
        else:
            cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f'"{product.name}" quantity updated in cart.')
    else:
        messages.success(request, f'"{product.name}" added to cart!')

    return redirect('/cart/')


@login_required
def update_cart(request, item_id):
    """Update quantity of a cart item"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity  = int(request.POST.get('quantity', 1))

    if quantity < 1:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    elif quantity > cart_item.product.stock:
        messages.warning(request, f'Only {cart_item.product.stock} items available.')
        cart_item.quantity = cart_item.product.stock
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated.')

    return redirect('/cart/')


@login_required
def remove_from_cart(request, item_id):
    """Remove a single item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'"{product_name}" removed from cart.')
    return redirect('/cart/')


@login_required
def clear_cart(request):
    """Remove all items from cart"""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared.')
    return redirect('/cart/')