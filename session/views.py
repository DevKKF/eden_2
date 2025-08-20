from django.shortcuts import redirect, render
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from session.models import Session



#Page des session de formation
def liste_sessions(request):

    session_formation = Session.objects.all().order_by('-id')

    context = {
        'session_formation': session_formation
    }

    return render(request, 'sessions/index.html', context)


def add_session(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')

        try:
            date_debut = datetime.strptime(date_debut_str, '%d-%m-%Y').date()
            date_fin = datetime.strptime(date_fin_str, '%d-%m-%Y').date()
        except ValueError:
            return JsonResponse({'success': False, 'error': "Format de date invalide."})

        if date_debut > date_fin:
            return JsonResponse({'success': False, 'error': "La date de fin ne peut pas être antérieure à la date de début."})

        Session.objects.create(
            nom=nom,
            description=description,
            date_debut=date_debut,
            date_fin=date_fin,
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': "Méthode non autorisée."})
