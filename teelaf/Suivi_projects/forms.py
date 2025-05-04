from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, HTML
from .models import SuiviProjet, SuiviInventaire

class SuiviProjetForm(forms.ModelForm):
    class Meta:
        model = SuiviProjet
        fields = '__all__'
        widgets = {
            'Date_de_début': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Date_de_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Participants': forms.Textarea(attrs={'rows': 2, 'class': 'textarea-low'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('Titre_et_zone', css_class='col-md-6'),
                Column('Date_de_début', css_class='col-md-6'),
            ),
            Row(
                Column('Date_de_fin', css_class='col-md-6'),
                Column('Budget_alloue', css_class='col-md-6'),
            ),
            Row(
                Column('Depenses_reelles', css_class='col-md-6'),
                Column('Subventions', css_class='col-md-6'),
            ),
            Row(
                Column('Participants', css_class='col-md-6'),
                Column('Beneficiaire', css_class='col-md-6'),
            ),
            Row(
                Column('Statuts', css_class='col-md-6'),
            ),
            Row(
                Column(
                    Submit('submit_projet', 'Enregistrer', css_class='btn btn-success me-2'),
                    HTML('<a class="btn btn-secondary" href="{% url \'suivi_projects_main\' %}">Annuler</a>'),
                    css_class='d-flex justify-content-end'
                ),
            ),
        )

class SuiviInventaireForm(forms.ModelForm):
    class Meta:
        model = SuiviInventaire
        fields = '__all__'
        widgets = {
            'Observation': forms.Textarea(attrs={'rows': 2, 'class': 'textarea-low'}),
            'Commentaire': forms.Textarea(attrs={'rows': 2, 'class': 'textarea-low'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('Description', css_class='col-md-6'),
                Column('Quantite', css_class='col-md-6'),
            ),
            Row(
                Column('Utiliser', css_class='col-md-6'),
                Column('En_stock', css_class='col-md-6'),
            ),
            Row(
                Column('Observation', css_class='col-md-6'),
                Column('Commentaire', css_class='col-md-6'),
            ),
            Row(
                Column(
                    Submit('submit_inventaire', 'Enregistrer', css_class='btn btn-success me-2'),
                    HTML('<a class="btn btn-secondary" href="{% url \'suivi_projects_main\' %}">Annuler</a>'),
                    css_class='d-flex justify-content-end'
                ),
            ),
        )