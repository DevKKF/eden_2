from django.shortcuts import redirect, render


#Page par défaut
def Accueil(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')

def erreur_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def erreur_401(request, exception):
    return render(request, 'errors/401.html', status=401)

def erreur_402(request, exception):
    return render(request, 'errors/402.html', status=402)

def erreur_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def erreur_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def erreur_419(request, exception):
    return render(request, 'errors/419.html', status=419)

def erreur_429(request, exception):
    return render(request, 'errors/429.html', status=429)

def erreur_500(request):
    return render(request, 'errors/500.html', status=500)

def erreur_503(request):
    return render(request, 'errors/503.html', status=503)