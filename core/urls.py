from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("cart/", views.cart, name='cart'),
    path("add_to_cart/", views.add_to_cart, name='add_to_cart'),
    path("clear_cart/", views.clear_cart, name='clear_cart'),
    path("cart_update_qnt/", views.cart_update_qnt, name='cart_update_qnt'),
    path("remove_from_cart/<int:prod_id>/", views.remove_from_cart, name='remove_from_cart'),
    
    path("product_by_id/<int:pid>/", views.product_by_id, name='product_by_id'),
    path("products/", views.products, name='products'),
    path("product/<str:cat>/", views.products, name='products_by_cat'),

    path("checkout/", views.checkout, name='checkout'), 
    path("invoice/<int:invoice_id>/", views.invoice, name='invoice'),
    # path("invoice/<int:invoice_id>/pdf", views.invoice_pdf, name='invoice_pdf'),
    path("orders/", views.orders, name='orders'),

    path("contact/", views.contact, name='contact'),
]
