from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
"""
class User(AbstractUser):
    name =  models.CharField(max_length=100)
    email = models.EmailField( unique=True)
    # avatar = models.ImageField(upload_to='user/avatars/', blank=True, null=True)
    
    phone = models.CharField(max_length=15, blank=True, null=True)

    is_customer = models.BooleanField(default=True)
    #is_vendor = models.BooleanField(default=False)  # future use (marketplace)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS =['email'] #when creating superuser

    def __str__(self):
        return self.username


class Address(AbstractUser):
    ADDRESS_TYPE = (
        ('billing','Billing'),
        ('shipping', 'Shipping'),
    )
    user = models.ForeignKey("User", on_delete=models.CASCADE,related_name='addresses')
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE)
    name = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.address_type}"
"""