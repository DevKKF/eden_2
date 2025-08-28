from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import uuid
import os

from parametre.models import TypeCours
from session.forms import SessionForm, CertificatForm, CoursForm
from session.models import Session, Certificat, Cours
from shared.enum import SessionStatut
from shared.helpers import convert_date_any_format


@login_required
def liste_sessions(request):

    statut_session = SessionStatut

    context = {
        'statut_session': statut_session
    }

    return render(request, 'sessions/index.html', context)


@login_required
def ajax_datatable_session(request):
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    draw = int(request.GET.get('draw', 1))

    sort_column_index = int(request.GET.get('order[0][column]', 0))
    sort_direction = request.GET.get('order[0][dir]', 'asc')

    search_date_deb = convert_date_any_format(request.GET.get('date_deb', ''))
    search_date_fn = convert_date_any_format(request.GET.get('date_fn', ''))
    search_statut_session = request.GET.get('statut_session', '')

    queryset = Session.objects.filter(deleted_at__isnull=True)

    # Filtres
    if search_date_deb and search_date_fn:
        # Sessions qui chevauchent avec la période recherchée
        queryset = queryset.filter(
            date_debut__lte=search_date_fn,
            date_fin__gte=search_date_deb
        )
    elif search_date_deb:
        queryset = queryset.filter(date_debut__gte=search_date_deb)
    elif search_date_fn:
        queryset = queryset.filter(date_fin__lte=search_date_fn)

    if search_statut_session:
        queryset = queryset.filter(statut_session=search_statut_session)

    # Tri
    sort_columns = {
        0: 'nom',
        1: 'date_publication',
        2: 'date_debut',
        3: 'date_fin',
        4: 'statut_session',
    }

    sort_column = sort_columns.get(sort_column_index, 'id')
    if sort_direction == 'desc':
        sort_column = '-' + sort_column

    queryset = queryset.order_by(sort_column)

    # Pagination
    total_records = queryset.count()

    if length == -1:
        page_queryset = queryset  # pas de pagination
    else:
        page_number = start // length + 1
        paginator = Paginator(queryset, length)
        try:
            page_queryset = paginator.page(page_number)
        except EmptyPage:
            page_queryset = paginator.page(paginator.num_pages)

        # Formatage des données
        data = []
        for sess in page_queryset:
            detail_url = reverse('detail_session', args=[sess.id])
            edit_url = reverse('update_session', args=[sess.id])

            # Bouton "Détails"
            actions_html = f'<a href="{detail_url}"><span class="btn btn-info btn-xs mr-5"><i class="fa fa-eye"></i></span></a>'

            # Bouton "Modifier"
            if request.user.is_superadmin:
                actions_html += f'<span class="btn_modifier_session btn btn-warning btn-xs mr-5" data-session_id="{sess.id}" data-model_name="session" data-modal_title="Modifier la session" data-href="{edit_url}"><i class="fa fa-edit"></i></span>'

            # Bouton "Supprimer"
            if request.user.is_superadmin:
                actions_html += f'<span class="btn_supprimer_session btn btn-danger btn-xs" data-session_id="{sess.id}"><i class="fa fa-trash-o"></i></span>'

            if sess.statut_session:
                statut_html = f'<span class="badge badge-{sess.statut_session.lower().replace(" ", "-")}">{sess.statut_session}</span>'
            else:
                statut_html = '<span class="badge badge-secondary">En attente</span>'

            data.append({
                "id": sess.id,
                "nom": sess.nom if sess.nom else "",
                "date_publication": sess.date_publication.strftime("%d/%m/%Y") if sess.date_publication else "",
                "date_debut": sess.date_debut.strftime("%d/%m/%Y") if sess.date_debut else "",
                "date_fin": sess.date_fin.strftime("%d/%m/%Y") if sess.date_fin else "",
                "nombre_inscrit": '',
                "statut": statut_html,
                "actions": actions_html,
            })

        return JsonResponse({
            "data": data,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "draw": draw,
        })


@login_required
def detail_session(request, session_id):
    session = Session.objects.get(id=session_id)

    if session is None:
        return redirect('sessions')

    statut_session = session.statut_session if session.statut_session else "En attente"
    classe_css_statut = statut_session.lower().replace(' ', '-')
    type_cours = TypeCours.objects.filter(deleted_at__isnull=True).order_by('libelle')

    context = {
        'session': session,
        'classe_css_statut': classe_css_statut,
        'type_cours': type_cours,
    }

    return render(request, 'sessions/detail_session.html', context)


@login_required
@transaction.atomic
def add_session(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.date_publication = timezone.now()
            session.created_at = timezone.now()
            session.created_by = request.user.id
            session.save()  # created_at, updated_at, created_by, updated_by remplis automatiquement

            return JsonResponse({
                'statut': 1,
                'message': "Session enregistrée avec succès !",
                'data': {}
            })

        return JsonResponse({
            'statut': 0,
            'message': "Erreurs de validation",
            'errors': form.errors
        })

    return JsonResponse({'statut': 0, 'message': "Méthode non autorisée"})


@login_required
@transaction.atomic
def update_session(request, session_id):
    try:
        session = Session.objects.get(id=session_id)
    except Session.DoesNotExist:
        return JsonResponse({'statut': 0, 'message': "Session non trouvée"})

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            session = form.save(commit=False)
            session.updated_at = timezone.now()
            session.updated_by = request.user.id
            session.save()
            return JsonResponse({
                'statut': 1,
                'message': "Session mise à jour avec succès !",
                'data': {}
            })

        return JsonResponse({
            'statut': 0,
            'message': "Erreurs de validation",
            'errors': form.errors
        })

    # GET : renvoyer le modal
    return render(request, 'partials/update_session_modal.html', {'session': session})


@login_required
def supprimer_session(request):
    if request.method == "POST":

        session_id = request.POST.get('session_id')

        session = Session.objects.get(id=session_id)
        if session.pk is not None:
            session.delete()
            response = {
                'statut': 1,
                'message': "Session supprimée avec succès !",
            }

        else:

            response = {
                'statut': 0,
                'message': "Session non trouvée !",
            }

        return JsonResponse(response)


@login_required
def certificats_session(request, session_id):
    session = Session.objects.get(id=session_id)

    if session is None:
        return redirect('sessions')

    statut_session = session.statut_session if session.statut_session else "En attente"
    classe_css_statut = statut_session.lower().replace(' ', '-')
    type_cours = TypeCours.objects.filter(deleted_at__isnull=True).order_by('libelle')

    certificat_session = Certificat.objects.filter(session_id=session.id, deleted_at__isnull=True).order_by('numero_certificat')

    context = {
        'session': session,
        'classe_css_statut': classe_css_statut,
        'certificat_session': certificat_session,
        'type_cours': type_cours,
    }

    return render(request, 'sessions/certificats.html', context)


@login_required
@transaction.atomic
def add_session_certificat(request, session_id):
    session = Session.objects.get(id=session_id)

    if session is None:
        redirect('detail_session', session_id=session_id)

    if request.method == 'POST':
        form = CertificatForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            date_debut_validite = form.cleaned_data['date_debut_validite']
            date_fin_validite = form.cleaned_data['date_fin_validite']
            session = get_object_or_404(Session, id=session_id)  # Assurez-vous que Session est importé

            # Préfixe basé sur l'année courante (2025)
            annee = timezone.now().year % 100  # Prend les deux derniers chiffres (25)
            prefixe = f"VHCI{annee:02d}"

            # Trouver le dernier numéro utilisé
            last_certificat = Certificat.objects.filter(numero_certificat__startswith=prefixe).order_by('-numero_certificat').first()
            start_num = 1
            if last_certificat:
                last_num = int(last_certificat.numero_certificat.replace(prefixe, '').lstrip('0') or '0')
                start_num = last_num + 1

            # Générer les certificats
            certificats = []
            for i in range(nombre):
                num = start_num + i
                numero_certificat = f"{prefixe}{num:03d}"  # Format avec 5 chiffres (ex: VHCI25001)
                certificats.append(Certificat(
                    id=uuid.uuid4(),
                    numero_certificat=numero_certificat,
                    date_debut_validite=date_debut_validite,
                    date_fin_validite=date_fin_validite,
                    session=session,
                    created_at = timezone.now(),
                    created_by = request.user.id,
                ))

            # Sauvegarder tous les certificats
            Certificat.objects.bulk_create(certificats)

            return JsonResponse({'statut': 1, 'message': f'{nombre} certificats générés avec succès.'})

        return JsonResponse({
            'statut': 0,
            'message': "Erreurs de validation",
            'errors': form.errors
        })
    else:
        redirect('detail_session', session_id=session_id)


@login_required
def delete_certificats(request):
    if request.method == 'POST':
        certificats_ids = request.POST.getlist('certificats_ids[]')
        try:
            certificats = Certificat.objects.filter(id__in=certificats_ids)
            if certificats.exists():
                certificats.delete()
                return JsonResponse({'statut': 1, 'message': 'Certificats supprimés avec succès.'})
            else:
                return JsonResponse({'statut': 0, 'message': 'Aucun certificat trouvé.'}, status=400)
        except Exception as e:
            return JsonResponse({'statut': 0, 'message': 'Erreur lors de la suppression.'}, status=500)
    return JsonResponse({'statut': 0, 'message': 'Méthode non autorisée.'}, status=405)


@login_required
@transaction.atomic
def add_session_cours(request, session_id):
    session = Session.objects.get(id=session_id)
    if request.method == 'POST':
        # Instancier le formulaire avec les données POST et les fichiers
        form = CoursForm(request.POST, request.FILES)

        if form.is_valid():
            # Préfixe basé sur l'année courante (2025)
            annee = timezone.now().year % 100  # Prend les deux derniers chiffres (25)
            prefixe = f"SCOU{annee:02d}"

            # Trouver le dernier numéro utilisé
            last_cours = Cours.objects.filter(numero_cours__startswith=prefixe).order_by('-numero_cours').first()
            start_num = 1
            if last_cours:
                last_num = int(last_cours.numero_cours.replace(prefixe, '').lstrip('0') or '0')
                start_num = last_num + 1

            # Si le formulaire est valide, les données sont nettoyées
            cours = form.save(commit=False)
            cours.session = session
            cours.numero_cours = f"{prefixe}{start_num:03d}"  # Format avec 5 chiffres (ex: SCOU25001)
            cours.date_publication = timezone.now()
            cours.created_at = timezone.now()
            cours.created_by = request.user.id
            cours.save()
            return JsonResponse({'statut': 1, 'message': 'Cours enregistré avec succès !'})

        return JsonResponse({
            'statut': 0,
            'message': "Erreurs de validation",
            'errors': form.errors
        })
    else:
        # Gérer la requête GET
        return redirect('detail_session', session_id=session_id)


@login_required
def cours_session(request, session_id):
    session = Session.objects.get(id=session_id)

    if session is None:
        return redirect('sessions')

    statut_session = session.statut_session if session.statut_session else "En attente"
    classe_css_statut = statut_session.lower().replace(' ', '-')
    type_cours = TypeCours.objects.filter(deleted_at__isnull=True).order_by('libelle')

    cours_session = Cours.objects.filter(session_id=session.id, deleted_at__isnull=True).order_by('-numero_cours')

    context = {
        'session': session,
        'classe_css_statut': classe_css_statut,
        'cours_session': cours_session,
        'type_cours': type_cours,
    }

    return render(request, 'sessions/cours.html', context)


@login_required
def detail_session_cours(request, cours_id):
    cours = Cours.objects.get(id=cours_id)

    if cours is None:
        return JsonResponse({
            'statut': 0,
            'message': "Cours non trouvé",
        })

    context = {
        'cours': cours,
    }

    return render(request, 'partials/detail_cours_modal.html', context)


@login_required
@transaction.atomic
def update_session_cours(request, cours_id):
    try:
        cours = Cours.objects.get(id=cours_id)
    except Cours.DoesNotExist:
        return JsonResponse({'statut': 0, 'message': "Cours non trouvé"})

    if request.method == 'POST':
        form = CoursForm(request.POST, request.FILES, instance=cours)
        if form.is_valid():
            # Sauvegarde sans commit pour comparer les fichiers
            new_cours = form.save(commit=False)

            # Vérifier et supprimer les anciens fichiers si remplacés
            if 'cours_video' in request.FILES and cours.cours_video:
                if cours.cours_video.path and os.path.isfile(cours.cours_video.path):
                    cours.cours_video.delete(save=False)

            if 'cours_audio' in request.FILES and cours.cours_audio:
                if cours.cours_audio.path and os.path.isfile(cours.cours_audio.path):
                    cours.cours_audio.delete(save=False)

            if 'cours_texte' in request.FILES and cours.cours_texte:
                if cours.cours_texte.path and os.path.isfile(cours.cours_texte.path):
                    cours.cours_texte.delete(save=False)

            # Mise à jour des métadonnées
            new_cours.updated_at = timezone.now()
            new_cours.updated_by = request.user.id
            new_cours.save()

            return JsonResponse({
                'statut': 1,
                'message': "Cours mis à jour avec succès !",
                'data': {}
            })

        return JsonResponse({
            'statut': 0,
            'message': "Erreurs de validation",
            'errors': form.errors
        })

    # GET : renvoyer le modal
    type_cours = TypeCours.objects.filter(deleted_at__isnull=True).order_by('libelle')
    return render(request, 'partials/update_cours_modal.html', {'cours': cours, 'type_cours': type_cours})


@login_required
def supprimer_cours(request):
    if request.method == "POST":

        cours_id = request.POST.get('cours_id')

        cours = Cours.objects.get(id=cours_id)
        if cours.pk is not None:
            cours.delete()
            response = {
                'statut': 1,
                'message': "Cours supprimé avec succès !",
            }

        else:
            response = {
                'statut': 0,
                'message': "Cours non trouvé !",
            }

        return JsonResponse(response)


@login_required
def activer_cours(request):
    if request.method == "POST":

        cours_id = request.POST.get('cours_id')

        cours = Cours.objects.get(id=cours_id)
        if cours.pk is not None:
            cours.statut_cours = SessionStatut.ENCOURS
            cours.date_activation = timezone.now()
            cours.save()

            response = {
                'statut': 1,
                'message': "Cours activé avec succès !",
            }

        else:
            response = {
                'statut': 0,
                'message': "Cours non trouvé !",
            }

        return JsonResponse(response)


