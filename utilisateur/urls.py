from django.urls import path
from utilisateur import views
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.Login, name="login"),
    path('home/', views.home, name="home"),
    path('logout', views.Logout, name="logout"),
    path('changer-mot-de-passe', views.change_password, name="change_password"),
]