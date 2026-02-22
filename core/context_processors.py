from .models import siteSettings

def site_settings(request):
    return{
        'site_settings':siteSettings.objects.first()
    }