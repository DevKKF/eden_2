from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Session


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['nom', 'date_debut', 'date_fin', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre certains champs obligatoires
        self.fields['nom'].required = True
        self.fields['date_debut'].required = True
        self.fields['date_fin'].required = True
        self.fields['description'].required = False

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not nom or not nom.strip():
            raise ValidationError("Le nom de la session est obligatoire.")
        return nom.strip()

    def clean_date_debut(self):
        date_debut = self.cleaned_data.get('date_debut')

        # Si c'est une chaîne, essayer de la convertir
        if isinstance(date_debut, str):
            if not date_debut.strip():
                raise ValidationError("La date de début est obligatoire.")

            # Essayer différents formats de date
            date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
            for date_format in date_formats:
                try:
                    date_debut = datetime.strptime(date_debut.strip(), date_format).date()
                    break
                except ValueError:
                    continue
            else:
                raise ValidationError("Format de date invalide. Utilisez le format YYYY-MM-DD.")

        if not date_debut:
            raise ValidationError("La date de début est obligatoire.")

        return date_debut

    def clean_date_fin(self):
        date_fin = self.cleaned_data.get('date_fin')

        # Si c'est une chaîne, essayer de la convertir
        if isinstance(date_fin, str):
            if not date_fin.strip():
                raise ValidationError("La date de fin est obligatoire.")

            # Essayer différents formats de date
            date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
            for date_format in date_formats:
                try:
                    date_fin = datetime.strptime(date_fin.strip(), date_format).date()
                    break
                except ValueError:
                    continue
            else:
                raise ValidationError("Format de date invalide. Utilisez le format YYYY-MM-DD.")

        if not date_fin:
            raise ValidationError("La date de fin est obligatoire.")

        return date_fin

    def clean(self):
        cleaned_data = super().clean()
        print('cleaned_data :', cleaned_data)

        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        # Vérifier que les deux dates sont présentes avant de les comparer
        if date_debut and date_fin:
            if date_debut > date_fin:
                raise ValidationError({
                    'date_fin': "La date de fin doit être postérieure à la date de début."
                })

        return cleaned_data