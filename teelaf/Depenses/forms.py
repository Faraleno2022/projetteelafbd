from django import forms
from .models import Depense, FraisFormation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class DepenseForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Depense
        fields = ['date', 'description', 'type', 'solde']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'solde': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'formulaire-bg'  # Fond bleu, police blanche
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='mb-3 col-md-6'),
                Column('type', css_class='mb-3 col-md-6'),
            ),
            'description',
            'solde',
            Submit('submit_depense', 'Enregistrer', css_class='btn btn-success')
        )

class FraisFormationForm(forms.ModelForm):
    date_inscription = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    inscription = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    avance_payer = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = FraisFormation
        fields = [
            'prenom_nom', 'date_inscription', 'formation_suivie',
            'frais_formation', 'inscription', 'avance_payer', 'date_fin'
        ]
        widgets = {
            'prenom_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'formation_suivie': forms.TextInput(attrs={'class': 'form-control'}),
            'frais_formation': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'formulaire-bg'  # Fond bleu, police blanche
        self.helper.layout = Layout(
            Row(
                Column('prenom_nom', css_class='mb-3 col-md-6'),
                Column('formation_suivie', css_class='mb-3 col-md-6'),
            ),
            Row(
                Column('date_inscription', css_class='mb-3 col-md-6'),
                Column('date_fin', css_class='mb-3 col-md-6'),
            ),
            Row(
                Column('frais_formation', css_class='mb-3 col-md-4'),
                Column('inscription', css_class='mb-3 col-md-4'),
                Column('avance_payer', css_class='mb-3 col-md-4'),
            ),
            Submit('submit_formation', 'Enregistrer', css_class='btn btn-success')
        )