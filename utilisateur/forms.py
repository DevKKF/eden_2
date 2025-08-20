from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Utilisateur

class CustomUserCreationForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Groupes"
    )

    class Meta:
        model = Utilisateur
        fields = ('username', 'nom', 'prenoms', 'email', 'telephone', 'groups', 'password1', 'password2')
