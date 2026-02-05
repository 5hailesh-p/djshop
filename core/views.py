from django.shortcuts import render
from django.http import HttpResponse
from .models import product

# Create your views here.
def home(request):

    context = {
        'products' : product.objects.filter(product_cat__in=['vehicel','accessories']),
    }

    return render(request, 'index.html', context)