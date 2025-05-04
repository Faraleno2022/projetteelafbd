from django.contrib import admin
from .models import SuiviApprenant

@admin.register(SuiviApprenant)
class SuiviApprenantAdmin(admin.ModelAdmin):
    list_display = ('ID_Apprenant', 'Nom_complet', 'Formation_suivi', 'Date_debut', 'Date_fin', 'Commentaire')
    search_fields = ('ID_Apprenant__Nom_complet', 'ID_Apprenant__Formation_suivi')
    list_filter = ('Commentaire', 'Date_debut', 'Date_fin')