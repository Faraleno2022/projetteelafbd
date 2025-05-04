from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import GrilleEvaluation
from learners.models import Learner

class GrilleEvaluationForm(forms.ModelForm):
    class Meta:
        model = GrilleEvaluation
        fields = [
            'learner', 'moyenne_ponderee', 'point_amelioration',
            'appreciation', 'numero_attestation', 'date_fin_formation', 'attestation'
        ]
        widgets = {
            'date_fin_formation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Affichage des IDs dans la liste déroulante
        self.fields['learner'].queryset = Learner.objects.all()
        self.fields['learner'].label_from_instance = lambda obj: f"{obj.student_id or obj.id}"

        self.fields['point_amelioration'].required = True
        self.fields['appreciation'].required = True
        # SUPPRIMER les widgets Textarea : les champs seront des input texte simples
        # self.fields['point_amelioration'].widget = forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
        # self.fields['appreciation'].widget = forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
        self.fields['date_fin_formation'].label = "Date de fin de formation"

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-container'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Row(
                Column('learner', css_class='mb-3 col-md-6'),
                Column('moyenne_ponderee', css_class='mb-3 col-md-6'),
            ),
            Row(
                Column('point_amelioration', css_class='mb-3 col-md-6'),
                Column('appreciation', css_class='mb-3 col-md-6'),
            ),
            Row(
                Column('numero_attestation', css_class='mb-3 col-md-6'),
                Column('date_fin_formation', css_class='mb-3 col-md-6'),
            ),
            Row(
                Column('attestation', css_class='mb-3 col-md-12'),
            ),
            Submit('submit', "Enregistrer", css_class="btn btn-primary mt-3 w-100")
        )