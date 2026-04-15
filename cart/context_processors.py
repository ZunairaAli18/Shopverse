from .models import Cart


def cart_count(request):
    """
    Injects cart_count into every template automatically.
    Shows 0 if user is not logged in or has no cart.
    """
    if request.user.is_authenticated and request.user.role == 'customer':
        try:
            cart  = Cart.objects.get(user=request.user)
            count = cart.get_total_items()
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0

    return {'cart_count': count}