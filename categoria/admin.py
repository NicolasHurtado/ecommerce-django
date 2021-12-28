from django.contrib import admin
from .models import Categoria

# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('Nombre_Categoria',)}
    list_display = ('Nombre_Categoria', 'slug')

admin.site.register(Categoria, CategoriaAdmin)