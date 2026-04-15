from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomerRegistrationForm, VendorRegistrationForm, LoginForm


def register_customer(request):
    """Customer registration view"""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)                          # log them in automatically
            messages.success(request, f'Welcome {user.username}! Account created.')
            return redirect('/products/')                 # customers go to shop
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CustomerRegistrationForm()

    return render(request, 'users/register_customer.html', {'form': form})


def register_vendor(request):
    """Vendor registration view"""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Set up your store.')
            return redirect('/stores/create/')            # vendors go to create store
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = VendorRegistrationForm()

    return render(request, 'users/register_vendor.html', {'form': form})


def login_view(request):
    """Login view for all user types"""
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user     = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')

                # ─── Role-based redirect ───────────────────
                if user.role == 'vendor':
                    return redirect('/stores/dashboard/')
                elif user.role == 'admin':
                    return redirect('/admin/')
                else:
                    return redirect('/products/')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/users/login/')