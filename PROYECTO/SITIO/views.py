from django.shortcuts import render
from django.http import HttpResponse
from .forms import *

# Create your views here.
def index(request):
    return render(request, "web/index.html")
