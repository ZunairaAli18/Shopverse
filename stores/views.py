from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Store
from .forms import StoreForm
from .decorators import vendor_required
from orders.models import OrderItem

def create_store(request):
    """
    Vendors create their store after registering.
    If vendor already has a store, redirect to dashboard.
    """
    if not request.user.is_authenticated:
        return redirect('/users/login/')

    if request.user.role != 'vendor':
        return redirect('/')

    # If vendor already has a store, go to dashboard
    if hasattr(request.user, 'store'):
        return redirect('/stores/dashboard/')

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)   # request.FILES for images
        if form.is_valid():
            store = form.save(commit=False)
            store.vendor = request.user                 # attach store to this vendor
            store.save()
            messages.success(request, 'Store created! Waiting for admin approval.')
            return redirect('/stores/dashboard/')
    else:
        form = StoreForm()

    return render(request, 'stores/create_store.html', {'form': form})


@vendor_required
def dashboard(request):
    """
    Vendor dashboard — shows store info, approval status, and stats.
    """
    try:
        store = request.user.store
    except Store.DoesNotExist:
        messages.warning(request, 'Please create your store first.')
        return redirect('/stores/create/')
    
    order_items     = OrderItem.objects.filter(vendor=store)
    total_orders    = order_items.count()
    pending_orders  = order_items.filter(status='pending').count()
    total_earnings  = sum(item.get_total_price() for item in order_items.filter(status='delivered'))
    context = {
        'store':          store,
        'total_products': store.total_products(),
        'total_orders':   total_orders,
        'pending_orders': pending_orders,
        'total_earnings': total_earnings,
    }
    return render(request, 'stores/dashboard.html', context)


@vendor_required
def edit_store(request):
    """Vendors can edit their store details"""
    try:
        store = request.user.store
    except Store.DoesNotExist:
        return redirect('/stores/create/')

    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated successfully.')
            return redirect('/stores/dashboard/')
    else:
        form = StoreForm(instance=store)

    return render(request, 'stores/edit_store.html', {'form': form})