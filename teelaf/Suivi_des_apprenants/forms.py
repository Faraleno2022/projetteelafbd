from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import SuiviApprenant
from learners.models import Learner

class SuiviApprenantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afficher uniquement l'ID (ou student_id) dans la liste déroulante
        self.fields['ID_Apprenant'].queryset = Learner.objects.all()
        self.fields['ID_Apprenant'].label_from_instance = lambda obj: f"{obj.student_id or obj.id}"

        # CRISPY LAYOUT
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-container'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Row(
                Column('ID_Apprenant', css_class='mb-3'),
                Column('Date_debut', css_class='mb-3'),
                Column('Date_fin', css_class='mb-3'),
            ),
            Row(
                Column('Poste_avant_teelaf', css_class='mb-3'),
                Column('Poste_apres_teelaf', css_class='mb-3'),
            ),
            Row(
                Column('Dernier_contact', css_class='mb-3'),
                Column('Commentaire', css_class='mb-3'),
            ),
        )

    class Meta:
        model = SuiviApprenant
        fields = [
            'ID_Apprenant', 'Date_debut', 'Date_fin',
            'Poste_avant_teelaf', 'Poste_apres_teelaf',
            'Dernier_contact', 'Commentaire'
        ]
        widgets = {
            'Date_debut': forms.DateInput(attrs={'type': 'date'}),
            'Date_fin': forms.DateInput(attrs={'type': 'date'}),
            'Dernier_contact': forms.DateInput(attrs={'type': 'date'}),
        }