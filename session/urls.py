from django.urls import path
from django.conf.urls.static import static

from eden import settings
from session import views


urlpatterns = [
    path('listes', views.liste_sessions, name="sessions"),
    path('ajax_datatable_session/', views.ajax_datatable_session, name="ajax_datatable_session"),
    path('add_session', views.add_session, name="add_session"),
    path('details/<str:session_id>', views.detail_session, name="detail_session"),
    path('update_session/<str:session_id>', views.update_session, name="update_session"),
    path("session/delete", views.supprimer_session, name='supprimer_session'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)