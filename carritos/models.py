from django.db import models
from store.models import Producto

# Create your models here.
class Carrito(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cart = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def subtotal(self):
        return self.product.precio * self.quantity

    def __unicode__(self):
        return self.product
    
