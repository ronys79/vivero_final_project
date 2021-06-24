from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0
    # admin has no need for this function
    if 'admin' in request.path:
        return {}
    else:
        try:
            # this get the cart contains session key
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            # cart count for log in user
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
            # this brings the corrsponding cart item
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            # cart item quantity
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)