from .models import Carrito, CartItem
from .views import _cart_id

def counter(request):
    cart_count=0

    try:
        cart = Carrito.objects.filter(cart_id=_cart_id(request))
        cart_items = CartItem.objects.all().filter(cart=cart[:1])

        for cart_item in cart_items:
            cart_count += cart_item.quantity

    except Carrito.DoesNotExist:
        cart_count=0
    
    return dict(cart_count=cart_count)