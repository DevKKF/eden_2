from django.urls import path
from utilisateur import views
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.Login, name="login"),
    path('home/', views.Home, name="home"),
    path('logout', views.Logout, name="logout"),
    path('changer-mot-de-passe', views.change_password, name="change_password"),

    path('utilisateurs', views.utilisateurs, name="utilisateurs"),
    path('add_utilisateur', views.add_utilisateur, name="add_utilisateur"),
    path('detail/<uuid:utilisateur_id>', views.detail_utilisateur, name="detail_utilisateur"),
    path('update_utilisateur/<uuid:utilisateur_id>', views.update_utilisateur, name="update_utilisateur"),
    path("utilisateur/delete", views.supprimer_utilisateur, name='supprimer_utilisateur'),
]