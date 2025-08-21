from django.conf import settings

def app_info(request):
    return {
        'NAME_APP': settings.NAME_APP,
        'VERSION_APP': settings.VERSION_APP,
    }
