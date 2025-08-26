from django.contrib.admin.actions import delete_selected
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from session.forms import SessionForm
from session.models import Session
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

    statut_session = session.statut_session if session.statut_session else "En attente"
    classe_css_statut = statut_session.lower().replace(' ', '-')

    context = {
        'session': session,
        'classe_css_statut': classe_css_statut,
    }

    return render(request, 'sessions/detail_session.html', context)


@login_required
@transaction.atomic
def add_session(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.date_publication = timezone.now()  # champ spécifique création
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
            form.save()  # updated_at et updated_by remplis automatiquement
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
