from django import forms
from .models import Learner
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div, Submit, Button

class LearnerForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = [
            'full_name', 'birth_date', 'gender', 'phone', 'email',
            'address', 'statut', 'desired_course', 'observation'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-container'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Row(
                Column('full_name', css_class='mb-3'),
                Column('birth_date', css_class='mb-3'),
            ),
            Row(
                Column('gender', css_class='mb-3'),
                Column('statut', css_class='mb-3'),
            ),
            Row(
                Column('phone', css_class='mb-3'),
                Column('email', css_class='mb-3'),
            ),
            Row(
                Column('address', css_class='mb-3'),
                Column('desired_course', css_class='mb-3'),
            ),
            Row(
                Column('observation', css_class='mb-3'),
            ),
            Div(
                Submit('submit', 'Enregistrer', css_class='btn btn-primary px-4 btn-animated me-2'),
                Button('cancel', 'Annuler', css_class='btn btn-secondary px-4 btn-animated', onclick="window.location.href='/learners/'"),
                css_class="form-footer text-center mt-3"
            )
        )