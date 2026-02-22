from django.shortcuts import render ,redirect
from .models import Product,Cart
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages

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
@require_POST
def add_to_cart(request):
    if request.method=='POST':
        product_id= request.POST.get('product_id')
        product  = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        item = product,
    )
    if not created:
        cart_item.quantity +=1
        cart_item.save()
    cart_count = Cart.objects.filter(user= request.user).count()

    # print(product)
    messages.success(request,"Added to cart ")
    return JsonResponse({
        'success':True,
        'cart_count':cart_count
    })

    # return render(request, 'cart.html')

def remove_from_cart(request,prod_id):
   cart_item = Cart.objects.get(user=request.user,item=prod_id)
   if cart_item:
    cart_item.delete();
    return redirect('cart')