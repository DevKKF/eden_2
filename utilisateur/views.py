from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.db.models import Q

from parametre.models import Departement
from utilisateur.models import Utilisateur


# Redirection et interdiction d'accès à la page de login après connexion
def user_is_authenticated_redirect(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirige l'utilisateur vers la page 'next' s'il existe, sinon vers 'home'
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        return view_func(request, *args, **kwargs)

    return wrapper


# Page de connexion
@user_is_authenticated_redirect
def Login(request):
    errors = {}
    if request.method == "POST":

        username_or_email_or_phone = request.POST['username']
        password = request.POST['password']

        if not username_or_email_or_phone:
            errors['username_or_email_or_phone'] = "Le login est obligatoire"
        if not password:
            errors['password'] = "Le mot de passe est obligatoire"
        if not errors:
            # Si aucun utilisateur n'est trouvé avec le username, on essaie avec l'email ou le numéro de téléphone
            try:
                utilisateur = Utilisateur.objects.get(Q(username=username_or_email_or_phone) |
                                        Q(email=username_or_email_or_phone) |
                                        Q(telephone=username_or_email_or_phone))
                utilisateur = authenticate(request, username=utilisateur.username, password=password)
            except Utilisateur.DoesNotExist:
                utilisateur = None  # Aucun utilisateur n'a été trouvé avec cet email

            if utilisateur is not None:
                login(request, utilisateur)
                next_url = request.session.pop('next_url', reverse('home'))
                return redirect(next_url)
            else:
                context = {
                    'values': request.POST,
                }
                messages.error(request, "Nom utilisateur ou email et mot de passe incorrect")
                return render(request, 'auth/login.html', context)

    context = {
        'errors': errors,
        'values': request.POST,
    }
    return render(request, 'auth/login.html', context)


# Page des tableaux de bord
@login_required
def Home(request):
    user = request.user
    if user is not None:
        login(request, user)
        departements = Departement.objects.all()
        return render(request, 'home.html', {'departements': departements})
    else:
        return redirect('login')


# Déconnexion
@login_required
def Logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return redirect('login')


# Changement de mot de passe
@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        pass
    return render(request, 'auth/change_password.html', {'user': user})