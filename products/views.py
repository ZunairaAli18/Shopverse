from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from stores.decorators import vendor_required
from .models import Product, Category
from .forms import ProductForm


@vendor_required
def add_product(request):
    """Vendors add a new product"""

    # Block unapproved vendors
    if not request.user.store.is_approved:
        messages.error(request, 'Your store must be approved before adding products.')
        return redirect('/stores/dashboard/')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product       = form.save(commit=False)
            product.store = request.user.store    # attach to vendor's store
            product.save()
            messages.success(request, f'"{product.name}" added successfully!')
            return redirect('/products/manage/')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProductForm()

    return render(request, 'products/add_product.html', {'form': form})


@vendor_required
def manage_products(request):
    """Vendors see and manage all their products"""
    products = Product.objects.filter(
        store=request.user.store
    ).order_by('-created_at')

    return render(request, 'products/manage_products.html', {'products': products})


@vendor_required
def edit_product(request, slug):
    """Vendors edit their own product"""
    product = get_object_or_404(Product, slug=slug, store=request.user.store)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{product.name}" updated successfully!')
            return redirect('/products/manage/')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {
        'form':    form,
        'product': product
    })


@vendor_required
def delete_product(request, slug):
    """Vendors delete their own product"""
    product = get_object_or_404(Product, slug=slug, store=request.user.store)

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'"{product_name}" deleted.')
        return redirect('/products/manage/')

    return render(request, 'products/delete_product.html', {'product': product})


def product_list(request):
    """
    Public page — all customers see active products from approved stores.
    """
    products = Product.objects.filter(
        status='active',
        store__is_approved=True
    ).order_by('-created_at')

    categories = Category.objects.all()

    # Filter by category if selected
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    return render(request, 'products/product_list.html', {
        'products':      products,
        'categories':    categories,
        'active_category': category_slug,
    })


def product_detail(request, slug):
    """Public product detail page"""
    product = get_object_or_404(Product, slug=slug, status='active')

    # Check if product is already in cart
    in_cart = False
    if request.user.is_authenticated:
        try:
            from cart.models import Cart
            cart = Cart.objects.get(user=request.user)
            in_cart = cart.items.filter(product=product).exists()
        except:
            in_cart = False

    return render(request, 'products/product_detail.html', {
        'product': product,
        'in_cart': in_cart,      # ← pass this to template
    })