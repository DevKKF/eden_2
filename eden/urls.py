from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from eden import views, settings


handler400 = 'eden.views.erreur_400'
handler401 = 'eden.views.erreur_401'
handler402 = 'eden.views.erreur_402'
handler403 = 'eden.views.erreur_403'
handler404 = 'eden.views.erreur_404'
handler419 = 'eden.views.erreur_419'
handler429 = 'eden.views.erreur_429'
handler500 = 'eden.views.erreur_500'
handler503 = 'eden.views.erreur_503'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.Accueil, name="accueil"),
    path('dashboard/', include('utilisateur.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
