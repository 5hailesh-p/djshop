from django.contrib import admin
from .models import siteSettings,contact
# Register your models here.

admin.site.register(siteSettings)
admin.site.register(contact)

class SiteSettingsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not siteSettings.objects.exists()





admin.site.site_header = "djshop Admin  "
admin.site.site_title = "dj shop"
admin.site.index_title = "Welcome to shop"
