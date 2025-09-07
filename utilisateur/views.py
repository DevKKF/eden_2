from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from shared.enum import SituationMatrimoniale, UserCompteStatut
from shared.helpers import relation_entre_table
from utilisateur.models import Utilisateur
from django.contrib.auth.models import Group


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

        now = timezone.now()

        cheminants = Utilisateur.objects.filter(user_etudiant=True).order_by('-numero_utilisateur')[:6]

        cheminant_mois_en_cours = Utilisateur.objects.filter(user_etudiant=True, date_joined__year = now.year, date_joined__month = now.month).count()

        context = {
            'cheminants': cheminants,
            'cheminant_mois_en_cours': cheminant_mois_en_cours,
        }
        return render(request, 'home.html', context)
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


@login_required
def utilisateurs(request):
    utilisateurs = Utilisateur.objects.exclude(user_etudiant=True).order_by('-id')
    situation_matrimoniale = SituationMatrimoniale

    context = {
        'utilisateurs': utilisateurs,
        'situation_matrimoniale': situation_matrimoniale,
    }

    return render(request, 'utilisateurs/utilisateurs.html', context)


@login_required
@transaction.atomic
def add_utilisateur(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        niveau_access = request.POST.get('niveau_access')
        situation_matrimoniale = request.POST.get('situation_matrimoniale')
        password1 = request.POST.get('password1')

        if Utilisateur.objects.filter(telephone=telephone).exists():
            return JsonResponse({'statut': 0, 'message': "Ce numéro de téléphone est déjà utilisé."})
        if Utilisateur.objects.filter(email=email).exists():
            return JsonResponse({'statut': 0, 'message': "Cet email est déjà utilisé."})
        if Utilisateur.objects.filter(username=username).exists():
            return JsonResponse({'statut': 0, 'message': "Cet login est déjà utilisé."})

        user_created = Utilisateur.objects.create(
            nom=nom,
            prenoms=prenoms,
            first_name=nom,
            last_name=prenoms,
            telephone=telephone,
            email=email if email else None,
            username=username,
            situation_matrimoniale=situation_matrimoniale,
            is_superuser = True if niveau_access == 'is_superadmin' else False,
            user_admin = True if niveau_access == 'is_admin' else False,
            is_staff = True,
            is_active = True,
            statut_compte=UserCompteStatut.ACTIVE,
        )
        user_created.set_password(password1)
        user_created.save()

        # Handle photo upload
        photo_name = request.FILES.get('photo')
        if photo_name:
            user_created.photo.save(photo_name.name, photo_name)
            user_created.save()

        return JsonResponse({
            'statut': 1,
            'message': "Utilisateur enregistré avec succès !",
            'data': {}
        })

    return JsonResponse({'statut': 0, 'message': "Méthode non autorisée"})


@login_required
def detail_utilisateur(request, utilisateur_id):
    try:
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
    except Utilisateur.DoesNotExist:
        return JsonResponse({'statut': 0, 'message': "Utilisateur non trouvé"})

    return render(request, 'partials/detail_utilisateur_modal.html', {'utilisateur':utilisateur})


@login_required
@transaction.atomic
def update_utilisateur(request, utilisateur_id):
    try:
        utilisateur = Utilisateur.objects.get(id=utilisateur_id)
    except Utilisateur.DoesNotExist:
        return JsonResponse({'statut': 0, 'message': "Utilisateur non trouvé"})

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        username = request.POST.get('username')
        niveau_access = request.POST.get('niveau_access')
        situation_matrimoniale = request.POST.get('situation_matrimoniale')
        password1 = request.POST.get('password1')

        # Vérifications unicité (exclure l’utilisateur courant)
        if Utilisateur.objects.filter(telephone=telephone).exclude(id=utilisateur.id).exists():
            return JsonResponse({'statut': 0, 'message': "Ce numéro de téléphone est déjà utilisé."})
        if Utilisateur.objects.filter(email=email).exclude(id=utilisateur.id).exists():
            return JsonResponse({'statut': 0, 'message': "Cet email est déjà utilisé."})
        if Utilisateur.objects.filter(username=username).exclude(id=utilisateur.id).exists():
            return JsonResponse({'statut': 0, 'message': "Ce login est déjà utilisé."})

        # Mise à jour des champs
        utilisateur.nom = nom
        utilisateur.prenoms = prenoms
        utilisateur.first_name = nom
        utilisateur.last_name = prenoms
        utilisateur.telephone = telephone
        utilisateur.email = email if email else None
        utilisateur.username = username
        utilisateur.situation_matrimoniale = situation_matrimoniale

        # Droits d’accès
        utilisateur.is_superuser = True if niveau_access == 'is_superadmin' else False
        utilisateur.user_admin = True if niveau_access == 'is_admin' else False
        utilisateur.user_etudiant = True if niveau_access == 'is_etudiant' else False
        utilisateur.is_staff = True
        utilisateur.is_active = True

        # Mise à jour du mot de passe seulement si renseigné
        if password1:
            utilisateur.set_password(password1)

        utilisateur.save()

        # Mise à jour photo si uploadée
        photo_name = request.FILES.get('photo')
        if photo_name:
            utilisateur.photo.save(photo_name.name, photo_name)
            utilisateur.save()

        return JsonResponse({
            'statut': 1,
            'message': "Utilisateur modifié avec succès !",
            'data': {}
        })

    situation_matrimoniale = SituationMatrimoniale
    context = {
        'utilisateur': utilisateur,
        'situation_matrimoniale': situation_matrimoniale,
    }
    return render(request, 'partials/update_utilisateur_modal.html', context)


@login_required
def supprimer_utilisateur(request):
    if request.method == "POST":
        utilisateur_id = request.POST.get('utilisateur_id')
        try:
            utilisateur = Utilisateur.objects.get(id=utilisateur_id)
        except Utilisateur.DoesNotExist:
            return JsonResponse({
                'statut': 0,
                'message': "Utilisateur non trouvé !",
            })

        if relation_entre_table(utilisateur):
            return JsonResponse({
                'statut': 0,
                'message': "Impossible de supprimer : cet utilisateur est encore utilisé dans une autre table.",
            })

        #utilisateur.delete()
        return JsonResponse({
            'statut': 1,
            'message': "Utilisateur supprimé avec succès !",
        })

