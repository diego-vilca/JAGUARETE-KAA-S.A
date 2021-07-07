from functools import total_ordering
from SITIO.models import Categoria
from SITIO.models import Carrito
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

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



def producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, "web/producto.html", {
        "producto": producto,
        #paso las categorias para el menu
        "lista_categorias": Categoria.objects.all(),
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

@permission_required('SITIO.change_producto')
def producto_editar(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":  
        form = FormProductoCustom(data=request.POST, files=request.FILES, instance=un_producto)
        if form.is_valid():
            form.save()
            return redirect("SITIO:index")
    else:
        form = FormProductoCustom(instance = un_producto)
        return render(request, 'web/producto_editar.html', {
            "form": form,
            #paso el producto para mostrar la imagen
            "producto": un_producto,
            #paso las categorias para el menu
            "lista_categorias": Categoria.objects.all(),
        })

def producto_eliminar(request, producto_id):
    un_producto = get_object_or_404(Producto, id=producto_id)
    un_producto.delete()
    return redirect("SITIO:index")

def buscador(request, categoria_id=""):
    if request.method == "POST":
        busqueda = request.POST['busqueda']
        #esta linea funciona
        # resultado = Producto.objects.filter(titulo__contains=busqueda)

        #el modulo Q permite me permite utilizar and/or en las consultas, distinct() me elimina las filas duplicadas
        resultado = Producto.objects.filter( Q(titulo__icontains = busqueda) | Q(descripcion_producto__icontains = busqueda)).distinct()
        

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

def acerca_de(request):
    return render(request,"web/acerca_de.html", {
        # paso las categorias para el menu
        "lista_categorias": Categoria.objects.all(),
    })

@login_required
@permission_required('SITIO.add_carrito')
def carrito(request, producto_id=''):
    
    #si entra un producto_id...
    if producto_id:
        carrito = Carrito.objects.filter(usuario=request.user.id).first()
        producto = Producto.objects.get(id=producto_id)
        

        #si el carrito del usuario existe...
        if carrito:
            if not producto in carrito.lista_productos.all():
                carrito.lista_productos.add(producto)
            else:
                carrito.lista_productos.remove(producto)

            #actualizo el precio total
            total = 0 
            for item in carrito.lista_productos.all():
                total += item.precio

            carrito.total_carrito = total
        
            #guardo el carrito
            carrito.save()

        else:
            usuario = User.objects.get(username=request.user)
            carrito = Carrito.objects.create(usuario = usuario)
            carrito.save()

            carrito.lista_productos.add(producto)
            carrito.total_carrito = producto.precio


        return render(request,"web/carrito.html", {
            # paso las categorias para el menu
            "lista_categorias": Categoria.objects.all(),
            "lista_carrito": carrito.lista_productos,
        })
    else:
        pass


def eliminar_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user.id).first()

    for producto in carrito.lista_productos.all():
        carrito.productos.remove(producto)

    carrito.total = 0
    carrito.save()

    return redirect(to="carrito")
            