from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from eden import settings
from session import views


urlpatterns = [
    path('listes', views.liste_sessions, name="sessions"),
    path('add_session', views.add_session, name="add_session"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)