from django.shortcuts import render ,redirect
from .models import Product,Cart, Order
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse,HttpResponse
from django.contrib import messages

# Create your views here.
# @login_required
def home(request): 
    fname = None
    if request.user.is_authenticated:
        fname =  request.user.first_name

    products = Product.objects.all()
    category =set({})

    for product in products:
        category.add(product.product_cat) 
     
    context = {
        # 'products' : Product.objects.filter(product_cat__in=['vehicel','accessories']),
        'products' : products,
        'category' :category,
        'fname' : fname,
    }

    return render(request, 'index.html', context)

def products(request,cat=''): 
    fname = None
    if request.user.is_authenticated:
        fname =  request.user.first_name
    all_prod =  Product.objects.all()
    if cat :
        products = Product.objects.filter(product_cat__in=[cat])
    else:
        products = all_prod
    category =set({})

    for product in all_prod:
        category.add(product.product_cat) 
     
    context = {
        'products' : products,
        # 'category' :category,
        'fname' : fname,
    }

    return render(request, 'products.html', context)

@login_required
def cart(request):
    if request.user.is_authenticated:
        fname =  request.user.first_name
    # carts = Cart.objects.filter(user=request.user)
    carts = Cart.objects.select_related('item').filter(user=request.user)
    for cart in carts:
        cart.total_price = cart.item.price * cart.quantity
 
    return render(request, 'cart.html',{'carts':carts,'fname':fname})
@require_POST
def add_to_cart(request):
    if request.method=='POST':
        product_id= request.POST.get('product_id')
        product_quantity= int(request.POST.get('product_quantity',1)) 
        product  = Product.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        item = product,
        defaults={'quantity':product_quantity},
    )
    
    if not created:
        cart_item.quantity += product_quantity
        cart_item.save()
    cart_count = Cart.objects.filter(user= request.user).count()

    # print(product)
    messages.success(request,"Added to cart ")
    # return JsonResponse({
    #     'success':True,
    #     'cart_count':cart_count
    # })

    return cart(request)
@login_required
def remove_from_cart(request,prod_id):
    cart_item = Cart.objects.get(user=request.user,item=prod_id)
    if cart_item:
        cart_item.delete();
    return redirect('cart')

@login_required
def cart_update_qnt(request):
    if request.method == 'POST':
        item_id  = request.POST.get('item_id')
        product_qnt  = request.POST.get('qnt')
 
        cart_item = Cart.objects.get(user=request.user,item=item_id)
        if cart_item:
            cart_item.quantity = product_qnt
            cart_item.save()

    return JsonResponse({
        'success':True,
    })

# products 

@login_required
def product_by_id(request,pid):
    product =  Product.objects.get(id=pid)  
    m_price , price = 20 , product.price
    off_pcnt =  100 - ((price * 100)/ (price+m_price)) 
    context = {
        'product': product,
        'off_pcnt': off_pcnt.__round__(2),
        'm_price':m_price,
        
    }
    return render(request, 'productVIew.html',context)

# order list 
@login_required
def orders(request):
    if request.method == 'POST':
        carts = Cart.objects.filter(user=request.user)
        
    orders =  Order.objects.filter(user=request.user)
    
    context = {
        'orders' : orders,
        'total_orders':orders.count()
    }
    return render(request, 'order.html',context)



@login_required
def checkout(request):
    carts = Cart.objects.select_related('item').filter(user= request.user)
    shipping, sub_total = 99, 0
 
    for cart in carts:
        cart.total_price = cart.item.price * cart.quantity
        sub_total+= cart.total_price
 
    context =  {
        'carts':carts,
        'shipping':shipping,
        'sub_total': sub_total,
    }

    return render(request, 'checkout.html', context) 


def contact(request): 
    return render(request, 'contact.html')



def custom_404(request, exception):
    return render(request, '404.html',status=404)