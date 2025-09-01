from django.urls import path
from django.conf.urls.static import static

from eden import settings
from session import views


urlpatterns = [
    path('listes', views.liste_sessions, name="sessions"),
    path('ajax_datatable_session/', views.ajax_datatable_session, name="ajax_datatable_session"),
    path('add_session', views.add_session, name="add_session"),
    path('detail/<uuid:session_id>', views.detail_session, name="detail_session"),
    path('update_session/<uuid:session_id>', views.update_session, name="update_session"),
    path("session/delete", views.supprimer_session, name='supprimer_session'),

    path("certificats/delete_certificats", views.delete_certificats, name='delete_certificats'),
    path('certificats/<uuid:session_id>', views.certificats_session, name="certificats_session"),
    path('add_session_certificat/<uuid:session_id>', views.add_session_certificat, name="add_session_certificat"),

    path('add_session_cours/<uuid:session_id>', views.add_session_cours, name="add_session_cours"),
    path('cours/<uuid:session_id>', views.cours_session, name="cours_session"),
    path('update_session_cours/<uuid:cours_id>', views.update_session_cours, name="update_session_cours"),
    path('cours/detail/<uuid:cours_id>', views.detail_session_cours, name="detail_session_cours"),
    path("cours/delete", views.supprimer_cours, name='supprimer_cours'),
    path("cours/activer", views.activer_cours, name='activer_cours'),

    path('add_session_cheminant/<uuid:session_id>', views.add_session_cheminant, name="add_session_cheminant"),
    path('cheminants/<uuid:session_id>', views.cheminant_session, name="cheminant_session"),
    path('cheminants/detail/<uuid:utilisateur_id>', views.detail_session_cheminant, name="detail_session_cheminant"),
    path('update_session_cheminants/<uuid:utilisateur_id>', views.update_session_cheminants, name="update_session_cheminants"),
    path("cheminants/delete", views.supprimer_cheminant, name='supprimer_cheminant'),

    path('add_qcm_cours_session/<uuid:session_id>', views.add_qcm_cours_session, name="add_qcm_cours_session"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
