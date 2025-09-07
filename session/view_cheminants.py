import urllib
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import default_storage
import uuid
import os

from parametre.models import Tribu, Departement
from shared.enum import Genre
from utilisateur.models import Utilisateur


@login_required
def cheminant_mois_en_cours(request):
    genre = Genre
    tribus = Tribu.objects.filter(deleted_at__isnull=True).order_by('libelle')
    departements = Departement.objects.filter(deleted_at__isnull=True).order_by('libelle')

    context = {
        'genre':genre,
        'tribus':tribus,
        'departements':departements,
    }

    return render(request, 'cheminants/index.html', context)


@login_required
def ajax_datatable_cheminant_mois_en_cours(request):
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    draw = int(request.GET.get('draw', 1))
    now = timezone.now()

    sort_column_index = int(request.GET.get('order[0][column]', 0))
    sort_direction = request.GET.get('order[0][dir]', 'asc')

    search_tribu = request.GET.get('tribu_id', '')
    search_departement = request.GET.get('departement_id', '')
    search_sexe = request.GET.get('sexe', '')

    queryset = Utilisateur.objects.filter(user_etudiant=True, date_joined__year=now.year, date_joined__month=now.month)

    # Filtres
    if search_tribu:
        queryset = queryset.filter(tribu_id=search_tribu)
    if search_departement:
        queryset = queryset.filter(departement_id=search_departement)
    if search_sexe:
        queryset = queryset.filter(sexe=search_sexe)

    # Tri
    sort_columns = {
        0: 'numero_utilisateur',
        1: 'nom',
        2: 'prenoms',
        3: 'tribu_id',
        4: 'departement_id',
        5: 'date_joined',
        6: 'statut_compte',
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
        for cheminant in page_queryset:
            detail_url = reverse('detail_cheminant_encours', args=[cheminant.id])

            # Bouton "Détails"
            actions_html = f'<a href="{detail_url}"><span class="btn btn-info btn-xs mr-5"><i class="fa fa-eye"></i></span></a>'

            if cheminant.statut_compte:
                statut_html = f'<span class="badge badge-{cheminant.statut_compte.lower().replace(" ", "-")}">{cheminant.statut_compte}</span>'
            else:
                statut_html = '<span class="badge badge-secondary">En attente</span>'

            image = ""
            if cheminant.photo:
                image = f'<img src="{cheminant.photo.url}" class="img-circle" width="35" alt="{ cheminant.nom } { cheminant.prenoms }">'
            else:
                adresse_ip = request.build_absolute_uri('/')
                image = f'<img src="{adresse_ip}static/dist/img/avatar.png" class="img-circle" width="35" alt="">'

            data.append({
                "id": cheminant.id,
                "photo": image,
                "numero": cheminant.numero_utilisateur if cheminant.numero_utilisateur else "",
                "nom_prenoms": f'{cheminant.nom} {cheminant.prenoms}' if cheminant.nom else "",
                "tribu": cheminant.tribu.libelle if cheminant.tribu else "",
                "departement": cheminant.departement.libelle if cheminant.departement else "",
                "date_inscription": cheminant.date_joined.strftime("%d/%m/%Y") if cheminant.date_joined else "",
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
def detail_cheminant_encours(request, cheminant_id):
    cheminant = Utilisateur.objects.get(id=cheminant_id)

    if cheminant is None:
        return redirect('cheminant_mois_en_cours')

    context = {
        'cheminant': cheminant,
    }

    return render(request, 'cheminants/detail_cheminant_encours.html', context)
