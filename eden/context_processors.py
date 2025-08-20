from django.conf import settings

def app_info(request):
    return {
        'APP_NAME': settings.APP_NAME,
        'APP_SUBTITLE': settings.APP_SUBTITLE,
        'APP_VERSION': settings.APP_VERSION,
    }
