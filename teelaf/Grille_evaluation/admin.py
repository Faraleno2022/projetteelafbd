from django.contrib import admin
from .models import GrilleEvaluation

@admin.register(GrilleEvaluation)
class GrilleEvaluationAdmin(admin.ModelAdmin):
    list_display = (
        'learner', 'moyenne_ponderee', 'point_amelioration', 'appreciation',
        'numero_attestation', 'date_fin_formation', 'attestation'
    )
    search_fields = ('learner__student_id', 'learner__full_name', 'numero_attestation')
    list_filter = ('date_fin_formation',)

# Si tu veux aussi voir les apprenants dans l'admin :
# from learners.models import Learner
# admin.site.register(Learner)