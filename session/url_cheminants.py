from django.urls import path
from django.conf.urls.static import static

from eden import settings
from session import view_cheminants


urlpatterns = [
    path('mois-en-cours', view_cheminants.cheminant_mois_en_cours, name="cheminant_mois_en_cours"),
    path('ajax_datatable_cheminant_mois_en_cours/', view_cheminants.ajax_datatable_cheminant_mois_en_cours, name="ajax_datatable_cheminant_mois_en_cours"),
    path('detail/<uuid:cheminant_id>', view_cheminants.detail_cheminant_encours, name="detail_cheminant_encours"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
