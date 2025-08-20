from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur
from .forms import CustomUserCreationForm

class UtilisateurAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = Utilisateur
    list_display = ('username', 'nom', 'prenoms', 'email', 'is_staff')

    # Pas besoin de réinserer `groups` ici, il y est déjà
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nom', 'prenoms', 'email', 'telephone', 'password1', 'password2', 'groups'),
        }),
    )

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('nom', 'prenoms', 'telephone', 'autre_telephone', 'situation_matrimoniale')
        }),
    )

admin.site.register(Utilisateur, UtilisateurAdmin)
