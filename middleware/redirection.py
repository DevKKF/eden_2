from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class RedirectToLastPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifie si l'utilisateur n'est pas connecté et veut accéder à une page autre que celle de connexion
        if not request.user.is_authenticated and request.path not in [reverse('login'), reverse('logout')]:
            # Enregistre l'URL de la page demandée si elle n'est pas la page de connexion
            request.session['next_url'] = request.path

        response = self.get_response(request)

        return response
