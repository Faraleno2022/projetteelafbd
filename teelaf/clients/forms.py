from datetime import date
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML, Div
from .models import ClientIndividuel, ClientEntreprise, ClientProspect

# Formulaire Client Individuel
class ClientIndividuelForm(forms.ModelForm):
    date_enregistrement = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        initial=date.today
    )
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        initial=date.today
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        initial=date.today
    )
    commentaire = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        required=False,
        label="Commentaire"
    )

    class Meta:
        model = ClientIndividuel
        # Utilise les champs réels de ton modèle
        fields = [
            'prenoms_nom', 'contact', 'email', 'type_service',
            'date_enregistrement', 'date_debut', 'date_fin',
            'commentaire', 'satisfaction'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('date_enregistrement', css_class='mb-3'),
            ),
            Row(
                Column('prenoms_nom', css_class='mb-3'),
                Column('contact', css_class='mb-3'),
            ),
            Row(
                Column('email', css_class='mb-3'),
                Column('type_service', css_class='mb-3'),
            ),
            Row(
                Column('date_debut', css_class='mb-3'),
                Column('date_fin', css_class='mb-3'),
            ),
            'commentaire',
            'satisfaction',
            Div(
                Submit('submit', 'Enregistrer', css_class='btn btn-light flex-fill'),
                HTML('<a href="{% url \'manage_clients_individuels\' %}" class="btn btn-outline-light flex-fill">Annuler</a>'),
                css_class='d-flex flex-column flex-md-row gap-2 mt-3'
            ),
        )

# Formulaire Client Entreprise
class ClientEntrepriseForm(forms.ModelForm):
    date_enregistrement = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        initial=date.today
    )
    date_debut = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        initial=date.today
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False,
        initial=date.today
    )
    commentaire = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        required=False,
        label="Commentaire"
    )

    class Meta:
        model = ClientEntreprise
        # Utilise les champs réels de ton modèle
        fields = [
            'beneficiaire', 'entreprise', 'numero', 'point_contact', 'email',
            'type_service', 'date_enregistrement', 'date_debut', 'date_fin',
            'commentaire', 'satisfaction'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('beneficiaire', css_class='mb-3'),
                Column('entreprise', css_class='mb-3'),
                Column('numero', css_class='mb-3'),
            ),
            Row(
                Column('point_contact', css_class='mb-3'),
                Column('email', css_class='mb-3'),
            ),
            Row(
                Column('type_service', css_class='mb-3'),
                Column('date_enregistrement', css_class='mb-3'),
                Column('date_debut', css_class='mb-3'),
                Column('date_fin', css_class='mb-3'),
            ),
            'commentaire',
            'satisfaction',
            Div(
                Submit('submit', 'Enregistrer', css_class='btn btn-light flex-fill'),
                HTML('<a href="{% url \'manage_clients_entreprises\' %}" class="btn btn-outline-light flex-fill">Annuler</a>'),
                css_class='d-flex flex-column flex-md-row gap-2 mt-3'
            ),
        )

# Formulaire Client Prospect
class ClientProspectForm(forms.ModelForm):
    commentaire = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        required=False,
        label="Commentaire"
    )

    class Meta:
        model = ClientProspect
        # Utilise les champs réels de ton modèle
        fields = [
            'prenoms_nom', 'contact', 'email', 'point_focal',
            'date_enregistrement', 'date_dernier_contact', 'deja_contact',
            'commentaire'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('prenoms_nom', css_class='mb-3'),
                Column('contact', css_class='mb-3'),
            ),
            Row(
                Column('email', css_class='mb-3'),
                Column('point_focal', css_class='mb-3'),
            ),
            Row(
                Column('date_enregistrement', css_class='mb-3'),
                Column('date_dernier_contact', css_class='mb-3'),
            ),
            'deja_contact',
            'commentaire',
            Div(
                Submit('submit', 'Enregistrer', css_class='btn btn-light flex-fill'),
                HTML('<a href="{% url \'manage_clients_prospects\' %}" class="btn btn-outline-light flex-fill">Annuler</a>'),
                css_class='d-flex flex-column flex-md-row gap-2 mt-3'
            ),
        )