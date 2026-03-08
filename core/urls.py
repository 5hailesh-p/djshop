from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("cart/", views.cart, name='cart'),
    path("add_to_cart/", views.add_to_cart, name='add_to_cart'),
    path("remove_from_cart/<int:prod_id>/", views.remove_from_cart, name='remove_from_cart'),
    
    path("product_by_id/<int:pid>/", views.product_by_id, name='product_by_id'),
    path("products/", views.products, name='products'),
    path("product/<str:cat>/", views.products, name='products_by_cat'),

    path("orders/", views.orders, name='orders'),

    path("contact/", views.contact, name='contact'),
]
