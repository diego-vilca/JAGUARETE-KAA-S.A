from django.urls import path
from django.urls import path
from . import views

app_name = "SITIO"
urlpatterns = [
    path('', views.index, name="index"),
    path('producto_alta', views.producto_alta, name="producto_alta"),
]