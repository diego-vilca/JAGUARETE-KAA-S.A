from django.urls import path
from django.urls import path
from . import views

app_name = "SITIO"
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:producto_id>', views.producto, name="producto"),
    path('producto_alta', views.producto_alta, name="producto_alta"),
    path('producto_editar/<int:producto_id>', views.producto_editar, name="producto_editar"),
    path('carrito/<int:producto_id>', views.carrito, name="carrito"),
    path('busqueda/<int:categoria_id>', views.buscador, name="buscador"),
    path('busqueda', views.buscador, name="buscador"),
]