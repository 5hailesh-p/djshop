from django.db import models

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

class contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=254)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
