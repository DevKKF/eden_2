from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

from parametre.models import TypeCours
from .models import Session, Cours


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

        date_debut = cleaned_data.get("date_debut")
        date_fin = cleaned_data.get("date_fin")

        # Vérifier que les deux dates sont présentes avant de les comparer
        if date_debut and date_fin:
            if date_debut > date_fin:
                raise ValidationError({
                    'date_fin': "La date de fin doit être postérieure à la date de début."
                })

        return cleaned_data


class CertificatForm(forms.Form):
    nombre = forms.IntegerField(
        label="Nombre de certificat à générer",
        min_value=1,
        max_value=300,
        widget=forms.TextInput(attrs={'class': 'form-control pull-right', 'onkeypress': 'isInputNumber(event)',
                                      'oninput': 'formatQuantite(this)'})
    )
    date_debut_validite = forms.DateField(
        label="Date début validité",
        widget=forms.DateInput(attrs={'class': 'form-control pull-right', 'type': 'date'})
    )
    date_fin_validite = forms.DateField(
        label="Date fin validité",
        widget=forms.DateInput(attrs={'class': 'form-control pull-right', 'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super(CertificatForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

    def clean_date_debut_validite(self):
        date_debut_validite = self.cleaned_data.get('date_debut_validite')

        # Si c'est une chaîne, essayer de la convertir
        if isinstance(date_debut_validite, str):
            if not date_debut_validite.strip():
                raise ValidationError("La date de début est obligatoire.")

            # Essayer différents formats de date
            date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
            for date_format in date_formats:
                try:
                    date_debut_validite = datetime.strptime(date_debut_validite.strip(), date_format).date()
                    break
                except ValueError:
                    continue
            else:
                raise ValidationError("Format de date invalide. Utilisez le format YYYY-MM-DD.")

        if not date_debut_validite:
            raise ValidationError("La date de début est obligatoire.")

        return date_debut_validite

    def clean_date_fin_validite(self):
        date_fin_validite = self.cleaned_data.get('date_fin_validite')

        # Si c'est une chaîne, essayer de la convertir
        if isinstance(date_fin_validite, str):
            if not date_fin_validite.strip():
                raise ValidationError("La date de fin est obligatoire.")

            # Essayer différents formats de date
            date_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']
            for date_format in date_formats:
                try:
                    date_fin_validite = datetime.strptime(date_fin_validite.strip(), date_format).date()
                    break
                except ValueError:
                    continue
            else:
                raise ValidationError("Format de date invalide. Utilisez le format YYYY-MM-DD.")

        if not date_fin_validite:
            raise ValidationError("La date de fin est obligatoire.")

        return date_fin_validite

    def clean(self):
        cleaned_data = super().clean()
        date_debut_validite = cleaned_data.get('date_debut_validite')
        date_fin_validite = cleaned_data.get('date_fin_validite')

        # Vérifier que les deux dates sont présentes avant de les comparer
        if date_debut_validite and date_fin_validite:
            if date_debut_validite > date_fin_validite:
                raise ValidationError({
                    'date_fin_validite': "La date de fin validité doit être postérieure à la date de début validité."
                })

        return cleaned_data


class CoursForm(forms.ModelForm):
    # On force type_cours_id pour correspondre au select du template
    type_cours_id = forms.UUIDField(required=True, widget=forms.HiddenInput())

    class Meta:
        model = Cours
        fields = ['titre', 'sous_titre', 'description',
                  'cours_video', 'cours_audio', 'cours_texte']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Marquer certains champs non obligatoires ici
        self.fields['cours_video'].required = False
        self.fields['cours_audio'].required = False
        self.fields['cours_texte'].required = False

    def clean(self):
        cleaned_data = super().clean()
        type_cours_id = self.data.get('type_cours_id')
        print('Type Cours ID:', type_cours_id)
        # Validation selon le type choisi
        if type_cours_id:
            from .models import TypeCours
            try:
                type_cours = TypeCours.objects.get(id=type_cours_id)
            except TypeCours.DoesNotExist:
                raise forms.ValidationError("Type de cours invalide")

            code = type_cours.code

            print('Code Type Cours:', code)

            if code == "VIDEOS" and not cleaned_data.get("cours_video"):
                self.add_error("cours_video", "Veuillez charger une vidéo")

            if code == "AUDIOS" and not cleaned_data.get("cours_audio"):
                self.add_error("cours_audio", "Veuillez charger un fichier audio")

            if code == "TEXTES" and not cleaned_data.get("cours_texte"):
                self.add_error("cours_texte", "Veuillez charger un fichier texte")

        return cleaned_data

    def save(self, commit=True):
        cours = super().save(commit=False)
        # Affecter le type de cours à partir de type_cours_id caché
        from .models import TypeCours
        type_cours_id = self.data.get("type_cours_id")
        if type_cours_id:
            cours.type_cours_id = type_cours_id

        if commit:
            cours.save()
        return cours
