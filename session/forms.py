from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from django.core.files.storage import default_storage
import os

from parametre.models import Tribu, Departement, Quartier
from shared.enum import StatutCertificat, SessionStatut
from utilisateur.models import Utilisateur
from .models import Session, Cours, Certificat, Inscription


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


class CheminantForm(forms.ModelForm):
    username = forms.CharField(required=False)
    certificat_id = forms.UUIDField(required=True)
    session_id = forms.UUIDField(required=True)
    tribu_id = forms.UUIDField(required=True)
    departement_id = forms.UUIDField(required=True)
    quartier_id = forms.UUIDField(required=True)

    class Meta:
        model = Utilisateur
        fields = [
            "nom", "prenoms", "sexe", "telephone", "autre_telephone",
            "indicatif_telephonique", "date_naissance", "situation_matrimoniale", "photo",
        ]

    def clean_telephone(self):
        telephone = self.cleaned_data.get("telephone")
        # Skip uniqueness check for the current instance during update
        if self.instance and self.instance.pk and self.instance.telephone == telephone:
            return telephone

        if Utilisateur.objects.filter(telephone=telephone).exists():
            raise ValidationError("Ce numéro de téléphone est déjà utilisé.")

        if Utilisateur.objects.filter(username=telephone).exists():
            raise ValidationError("Ce numéro de téléphone est déjà utilisé comme identifiant.")

        return telephone

    def clean_certificat_id(self):
        certificat_id = self.cleaned_data.get("certificat_id")
        try:
            certificat = Certificat.objects.get(id=certificat_id)
        except Certificat.DoesNotExist:
            raise ValidationError("Certificat introuvable.")

        # Ignorer la vérification d'utilisation pour l'instance actuelle pendant la mise à jour
        if self.instance and self.instance.pk and self.instance.certificat_id == certificat_id:
            return certificat

        if certificat.date_utilisation is not None:
            raise ValidationError("Ce certificat est déjà utilisé.")

        return certificat

    def clean_session_id(self):
        session_id = self.cleaned_data.get("session_id")
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            raise ValidationError("Session introuvable.")
        return session

    def clean_tribu_id(self):
        tribu_id = self.cleaned_data.get("tribu_id")
        try:
            tribu = Tribu.objects.get(id=tribu_id)
        except Tribu.DoesNotExist:
            raise ValidationError("Tribu introuvable.")
        return tribu

    def clean_departement_id(self):
        departement_id = self.cleaned_data.get("departement_id")
        try:
            departement = Departement.objects.get(id=departement_id)
        except Departement.DoesNotExist:
            raise ValidationError("Département introuvable.")
        return departement

    def clean_quartier_id(self):
        quartier_id = self.cleaned_data.get("quartier_id")
        try:
            quartier = Quartier.objects.get(id=quartier_id)
        except Quartier.DoesNotExist:
            raise ValidationError("Quartier introuvable.")
        return quartier

    def save(self, commit=True):
        utilisateur = super().save(commit=False)

        # Définir les attributs utilisateur
        utilisateur.username = self.cleaned_data["telephone"]
        utilisateur.first_name = self.cleaned_data["nom"]
        utilisateur.last_name = self.cleaned_data["prenoms"]
        utilisateur.is_superuser = False
        utilisateur.is_staff = True
        utilisateur.is_active = True

        # Cas modification
        if self.instance.pk:
            if 'photo' in self.files:
                # Supprimer l'ancienne photo si elle existe
                if self.instance.photo and default_storage.exists(self.instance.photo.path):
                    try:
                        default_storage.delete(self.instance.photo.path)
                        print(f"Ancienne photo supprimée : {self.instance.photo.path}")
                    except Exception as e:
                        print(f"Erreur suppression ancienne photo : {e}")

                # Remplacer par la nouvelle photo
                utilisateur.photo = self.files['photo']
        else:
            utilisateur.set_password('12345678')
            if 'photo' in self.files:
                utilisateur.photo = self.files['photo']

        # Assign related fields
        certificat = self.cleaned_data["certificat_id"]
        session = self.cleaned_data["session_id"]
        tribu = self.cleaned_data["tribu_id"]
        departement = self.cleaned_data["departement_id"]
        quartier = self.cleaned_data["quartier_id"]

        utilisateur.certificat = certificat
        utilisateur.session = session
        utilisateur.tribu = tribu
        utilisateur.departement = departement
        utilisateur.quartier = quartier

        if commit:
            utilisateur.save()

        return utilisateur


class InscriptionForm(forms.ModelForm):
    utilisateur = forms.ModelChoiceField(
        queryset=Utilisateur.objects.all(),
        required=True,
        label="Utilisateur"
    )
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        required=True,
        label="Session"
    )
    certificat = forms.ModelChoiceField(
        queryset=Certificat.objects.all(),
        required=True,
        label="Certificat"
    )
    statut_inscription = forms.ChoiceField(
        choices=SessionStatut.choices,
        required=True,
        initial=SessionStatut.ENCOURS,
        label="Statut de l'inscription"
    )

    class Meta:
        model = Inscription
        fields = ['utilisateur', 'session', 'certificat', 'statut_inscription']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-remplir la session avec session_id si fourni
        if 'session_id' in self.initial:
            self.fields['session'].queryset = Session.objects.filter(id=self.initial['session_id'])
