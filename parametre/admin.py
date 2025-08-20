from django.contrib import admin

# Register your models here.

from parametre.models import Quartier, Departement, Tribu, TypeCours

@admin.register(Quartier)
class QuartierAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'created_at', 'updated_at')
    search_fields = ('libelle',)
    list_filter = ('created_at', 'updated_at')

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'created_at', 'updated_at')
    search_fields = ('libelle',)
    list_filter = ('created_at', 'updated_at')

@admin.register(Tribu)
class TribuAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'created_at', 'updated_at')
    search_fields = ('libelle',)
    list_filter = ('created_at', 'updated_at')

@admin.register(TypeCours)
class TypeCoursAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'created_at', 'updated_at')
    search_fields = ('libelle',)
    list_filter = ('created_at', 'updated_at')


