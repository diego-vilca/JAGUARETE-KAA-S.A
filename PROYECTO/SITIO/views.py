from SITIO.models import Categoria
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .forms import *

# Create your views here.
def index(request):
    if "carrito" not in request.session:
        request.session["carrito"] = []
    return render(request,"web/index.html", {
        "lista_productos": Producto.objects.all(),
        "lista_categorias": Categoria.objects.all(),
        "carrito": request.session["carrito"],
    })

# def producto_alta(request):
#     #VueloForm = modelform_factory(Vuelo, fields=("origen", "destino", "duracion"))
#     if request.method == "POST":
#         form = FormProductoCustom(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = FormProductoCustom()
#         return render(request, "web/producto_alta.html", {
#             "form": form,
#         })

def producto_alta(request):
    if request.method == "POST":
        #user = User.objects.get(username=request.user)
        form = FormProductoCustom(request.POST, request.FILES, instance=Producto(imagen=request.FILES['imagen']))      
        if form.is_valid():
            form.save()
            return redirect("SITIO:index")          
    else:
        form = FormProductoCustom()
        return render(request, "web/producto_alta.html", {
            "form": form
        })
        