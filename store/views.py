from django.core import paginator
from django.shortcuts import get_object_or_404, render

from carritos.models import CartItem
from carritos.views import _cart_id
from .models import Producto
from categoria.models import Categoria
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.
def store(request, categoria_slug=None):
    categorias = None
    productos = None
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, disponible=True)
        paginator = Paginator(productos, 5)
        #Obtiene el numero de pagina para la paginación
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        producto_count = productos.count()
    else:
        productos = Producto.objects.all().filter(disponible=True)
        paginator = Paginator(productos, 5)
        #Obtiene el numero de pagina para la paginación
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        producto_count = productos.count()

    context = {
        'productos' : paged_products,
        'producto_count': producto_count,
    }
    return render(request, 'store/store.html', context)

def detalle_producto(request, categoria_slug, producto_slug):
    try:
        single_product = Producto.objects.get(categoria__slug=categoria_slug, slug= producto_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/detalle_producto.html', context)