from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("add_to_cart/<int:prod_id>/", views.add_to_cart, name='add_to_cart'),
    path("cart/", views.cart, name='cart'),
]
