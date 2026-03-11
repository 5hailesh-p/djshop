from django.shortcuts import render ,redirect
from .models import Product,Cart, Order,OrderItem,Subscribe,Contact
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
 
import random
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

@login_required
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
 
    messages.success(request,"Added to cart ") 
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

# @login_required
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

def clear_cart(request):
     
    Cart.objects.filter(user=request.user).delete()
    return True
    
# order list 
@login_required
def orders(request):
    orders =  Order.objects.filter(user=request.user).order_by('created_at')
    if request.method == 'POST':
        sub_total = int(request.POST.get('sub_total'))
        shipping = int(request.POST.get('shipping'))

        carts = Cart.objects.select_related('item').filter(user=request.user)
        lst = {
            "product":[],
            "product_name":[],
            "price":[],
            "quantity":[],
        }

        while True:
            rand_id = gen_rand()
            inv = OrderItem.objects.filter(invoice_id=rand_id)
            if not inv :
                # print('matched')
                # rand_id = gen_rand()
                break
        
        for cart in carts: 
          
            lst['product'].append(cart.item.id)
            lst['product_name'].append(cart.item.product_name)
            lst['price'].append(cart.item.price)
            lst['quantity'].append(cart.quantity)
           
            orders =  Order.objects.create(
                user=request.user,
                item=cart.item,
                price=cart.item.price,
                paid_amt=sub_total+shipping,
                quantity=cart.quantity, 
                invoice_id = rand_id,
            )
            
            product = Product.objects.get(id=cart.item.id)
            product.product_quantity -= cart.quantity
            product.save()  
        invoice = OrderItem.objects.create(
                user=request.user,
                order=orders,
                invoice_id=rand_id,
                product= lst['product'],
                product_name=lst['product_name'],
                price=lst['price'],
                quantity=lst['quantity'],
            )
        invoice.save() 
        invoice.order= orders
        invoice.save()
        orders.save() 
        
        cleared = clear_cart(request) 
        return JsonResponse({
            'success':True,
            'cart-cleared':cleared,
        })

    context = {
        'orders' : orders,
        'total_orders':orders.count()
    }
    return render(request, 'order.html',context)


@login_required
def checkout(request):
    carts = Cart.objects.select_related('item').filter(user= request.user)
    shipping, sub_total = 99 if carts.__len__() > 0 else 00 , 0
 
    for cart in carts:
        cart.total_price = cart.item.price * cart.quantity
        sub_total+= cart.total_price
 
    context =  {
        'carts':carts,
        'shipping':shipping,
        'sub_total': sub_total,
    }

    return render(request, 'checkout.html', context) 

@login_required
def invoice(request,invoice_id):
     
    order_item =  OrderItem.objects.select_related('order').get(user=request.user,invoice_id=invoice_id)

    products = order_item.product
    names = order_item.product_name
    prices = order_item.price
    quantities = order_item.quantity

    items = zip(products, names, prices, quantities)

    total = [p* q for p,q in zip(prices,quantities)]

 
    context = { 
        "carts" :items,
        "total" :sum(total),
        "shipping" :99,
        "issue":order_item.order.created_at,
        "invoice_id":invoice_id,

    }
    return render(request, "invoice.html", context )

# @login_required
# def invoice_pdf(request,invoice_id):
    
#     order_item =  OrderItem.objects.select_related('order').get(user=request.user,invoice_id=invoice_id)

#     products = order_item.product
#     names = order_item.product_name
#     prices = order_item.price
#     quantities = order_item.quantity

#     items = zip(products, names, prices, quantities)

#     total = [p* q for p,q in zip(prices,quantities)]

 
#     context = { 
#         "carts" :items,
#         "total" :sum(total),
#         "shipping" :99,
#         "issue":order_item.order.created_at,
#         "invoice_id":invoice_id,

#     }
#     html_string =  render_to_string("invoice.html", context )
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = f'attachment;filename="invoice{invoice_id}.pdf"'
#     # HTML(
#     #     string=html_string,
#     #     base_url=request.build_absolute_uri(),

#     # ).write_pdf(response)
#     # return render(request, "invoice.html", context )


@require_POST
def subscribe(request): 
    if request.method == 'POST':
        email = request.POST.get('email')
        added = Subscribe.objects.create(
            email=email,
        )

        return JsonResponse({
            'success':True,
        })


def contact(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        cont = Contact.objects.create(
            name= name,
            phone= phone,
            email= email,
            subject= subject,
            message= message,

        )
        if cont :
            messages.success(request,"Successfully Submitted")
        else:
            messages.error(request,"Invalid details")


    return render(request, 'contact.html')




def custom_404(request, exception):
    return render(request, '404.html',status=404)


# helper functions
def gen_rand():
    return random.randint(100000,999999)