from django.shortcuts import get_object_or_404, render
from .models import Producto
from categoria.models import Categoria

# Create your views here.
def store(request, categoria_slug=None):
    categorias = None
    productos = None
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug=categoria_slug)
        productos = Producto.objects.filter(categoria=categorias, disponible=True)
        producto_count = productos.count()
    else:
        productos = Producto.objects.all().filter(disponible=True)
        producto_count = productos.count()

    context = {
        'productos' : productos,
        'producto_count': producto_count,
    }
    return render(request, 'store/store.html', context)

def detalle_producto(request, categoria_slug, producto_slug):
    try:
        single_product = Producto.objects.get(categoria__slug=categoria_slug, slug= producto_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_product': single_product
    }
    return render(request, 'store/detalle_producto.html', context)