from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from carritos.models import Carrito, CartItem
from store.models import Producto

# Create your views here.

#Retorna la Sesion
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Producto.objects.get(id=product_id)
    try:
        cart = Carrito.objects.get(cart_id=_cart_id(request))
    except Carrito.DoesNotExist:
        cart = Carrito.objects.create(
            cart_id = _cart_id(request)
        )
    #Se dispara el evento y se registra en la db
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        cart_item.save()
    return redirect("carrito")

def remove_cart(request, product_id):
    cart = Carrito.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Producto, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity>1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect("carrito")

def remove_cart_item(request, product_id):
    cart = Carrito.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Producto, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("carrito")

def carrito(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Carrito.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.precio * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass # Solo ignora la excepcion

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)