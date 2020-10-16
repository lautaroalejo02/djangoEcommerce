from django.contrib import admin

from gestionPedidos.models import Clientes,Articulos,Pedidos,Categoria,Post

# Register your models here.

class ClientesAdmin(admin.ModelAdmin):
    list_display=("nombre","direccion","tfno")
    search_fields=("nombre","tfno")
class ArticulosAdmin(admin.ModelAdmin):
    list_filter = ("seccion",)

class PedidosAdmin(admin.ModelAdmin):
    list_display = ("numero","fecha")
    list_filter=("fecha"),
    date_hierarchy="fecha" #MENU MIGAS DE PAN
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id","nombre")
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo","contenido")
admin.site.register(Clientes,ClientesAdmin)
admin.site.register(Articulos,ArticulosAdmin)
admin.site.register(Pedidos,PedidosAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Post,PostAdmin)

