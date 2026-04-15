from django.shortcuts import redirect
from django.contrib import messages


def vendor_required(view_func):
    """
    Decorator that:
    - Redirects to login if not authenticated
    - Redirects to home if logged in but not a vendor
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('/users/login/')

        if request.user.role != 'vendor':
            messages.error(request, 'This page is for vendors only.')
            return redirect('/')

        return view_func(request, *args, **kwargs)

    return wrapper