from django.urls import path
from . import views

urlpatterns = [
    path('',views.store, name="store"),
    path('<slug:categoria_slug>', views.store, name='productos_por_categoria'),
    path('<slug:categoria_slug>/<slug:producto_slug>/', views.detalle_producto, name='detalle_producto')
]
