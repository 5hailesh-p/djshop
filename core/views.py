from django.shortcuts import render 
from .models import product
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request): 
    context = {
        # 'products' : product.objects.filter(product_cat__in=['vehicel','accessories']),
        # 'products' : product.objects.all(),
        'fname' : request.user.first_name,
    }

    return render(request, 'index.html', context)