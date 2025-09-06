from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Utilisateur

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('username', 'nom', 'prenoms', 'email', 'telephone', 'password1', 'password2')
