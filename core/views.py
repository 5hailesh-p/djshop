from django.shortcuts import render 
from .models import product

# Create your views here.
def home(request):

    context = {
        # 'products' : product.objects.filter(product_cat__in=['vehicel','accessories']),
        'products' : product.objects.all(),
    }

    return render(request, 'index.html', context)