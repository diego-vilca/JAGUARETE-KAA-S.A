from django import forms
from .models import Producto

class FormProductoCustom(forms.ModelForm):

    #campos del modelo
    class Meta:
        model = Producto
        fields = ('titulo', 'categoria', 'precio', 'descripcion_producto', 'imagen')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'prod_titulo'}),
            'precio': forms.TextInput(attrs={'class': 'prod_precio'}),
            'descripcion': forms.Textarea(attrs={'class': 'prod_descripcion'}),
            'imagen': forms.FileInput(attrs={'name':'imagen_adjunta', 'class': 'prod_imagen'}),
        }