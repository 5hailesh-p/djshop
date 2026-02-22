from django.shortcuts import render 
from .models import Product,Cart
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def home(request): 
    fname = None
    if request.user.is_authenticated:
        fname =  request.user.first_name
    context = {
        # 'products' : Product.objects.filter(product_cat__in=['vehicel','accessories']),
        'products' : Product.objects.all(),
        'fname' : fname,
    }

    return render(request, 'index.html', context)

@login_required
def cart(request):
    if request.user.is_authenticated:
        fname =  request.user.first_name
    carts = Cart.objects.filter(user=request.user)
    for cart in carts:
        cart.total_price = cart.item.price * cart.quantity
 
    return render(request, 'cart.html',{'carts':carts,'fname':fname})

def add_to_cart(request):
    # if request.method=='POST':
        # product_id= request.POST.get('')
    return render(request, 'cart.html')

def remove_from_cart(request):

    return render(request, 'cart.html')