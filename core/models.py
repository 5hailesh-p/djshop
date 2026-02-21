from django.db import models
from django.contrib.auth.models import User
from .info import PRODUCT_CATAEGORY
# Create your models here.
class siteSettings(models.Model):
    site_name = models.CharField( max_length=100)
    logo = models.ImageField(upload_to='logo/',blank=True,null=True)

    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    
    # social links
    instagram = models.URLField(blank=True,null=True)
    telegram = models.URLField(blank=True,null=True)
    facebook = models.URLField(blank=True,null=True)
    twitter = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.site_name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=254)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    # pid = models.IntegerField(max_length=254,unique=True,)
    product_name = models.CharField(max_length=254)
    product_desc = models.TextField()
    product_cat = models.CharField(max_length=100, choices=PRODUCT_CATAEGORY,default=PRODUCT_CATAEGORY['fruits'])
    price = models.IntegerField()
    product_img  = models.ImageField(upload_to='product/img/')
    product_quantity = models.IntegerField(default=0, null=True)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    cart_user = models.ForeignKey(User, on_delete=models.CASCADE)
