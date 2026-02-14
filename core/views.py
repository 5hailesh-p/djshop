from django.shortcuts import render 
from .models import product
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def home(request): 
    fname = None
    if request.user.is_authenticated:
        fname =  request.user.first_name
    context = {
        # 'products' : product.objects.filter(product_cat__in=['vehicel','accessories']),
        'products' : product.objects.all(),
        'fname' : fname,
    }

    return render(request, 'index.html', context)