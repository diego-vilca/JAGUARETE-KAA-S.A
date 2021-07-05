from SITIO.models import Categoria
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

# Create your views here.
def index(request):
    if "carrito" not in request.session:
        request.session["carrito"] = []

    
    lista_productos = Producto.objects.all()
    #devuelvo la lista invertida
    lista_invertida = lista_productos[::-1]
    #seteo los ultimos 3 productos en una lista
    lista_imagenes = lista_invertida[0:3]
    #seteo los productos del 4 al 10
    lista_plana = lista_invertida[3:10]
    
    return render(request,"web/index.html", {
        "lista_productos_imagenes": lista_imagenes,
        "lista_productos": lista_plana,
        #paso las categorias para el menu
        "lista_categorias": Categoria.objects.all(),
        "carrito": request.session["carrito"],
    })

@permission_required('SITIO.add_producto')
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
            "form": form,
            #paso las categorias para el menu
            "lista_categorias": Categoria.objects.all(),
        })


def producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, "web/producto.html", {
        "producto": producto,
        #paso las categorias para el menu
        "lista_categorias": Categoria.objects.all(),
    })

@permission_required('SITIO.add_carrito')
def carrito(request, producto_id):
    pass


def buscador(request, categoria_id=""):
    # return render(request, 'web/busqueda.html', {
    #     "categoria":categoria_id
    # })
    if request.method == "POST":
        busqueda = request.POST['busqueda']
        resultado = Producto.objects.filter(titulo__contains=busqueda)
        #resultado_contenido = Producto.objects.filter(descripcion_producto__contains=busqueda)
        

        return render(request, "web/busqueda.html", {
            "busqueda" : busqueda,
            "resultado": resultado,
            #paso las categorias para el menu
            "lista_categorias": Categoria.objects.all(),
        })
    else:
        una_categoria = get_object_or_404(Categoria, id=categoria_id)
        queryset = Producto.objects.all()
        queryset = queryset.filter(categoria=una_categoria)
        return render(request, "web/busqueda.html", {
            # paso las categorias para el menu
            "lista_categorias": Categoria.objects.all(),
            "lista_productos":queryset,
            "categoria_seleccionada": una_categoria

        })
