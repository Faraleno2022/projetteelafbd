from django.contrib import admin
from .models import SuiviProjet, SuiviInventaire

@admin.register(SuiviProjet)
class SuiviProjetAdmin(admin.ModelAdmin):
    list_display = (
        'Titre_et_zone',
        'Date_de_début',
        'Date_de_fin',
        'Budget_alloue',
        'Depenses_reelles',
        'Subventions',
        'Participants',
        'Beneficiaire',
        'Statuts'
    )
    search_fields = ('Titre_et_zone', 'Beneficiaire', 'Statuts')
    list_filter = ('Statuts', 'Date_de_début', 'Date_de_fin')

@admin.register(SuiviInventaire)
class SuiviInventaireAdmin(admin.ModelAdmin):
    list_display = (
        'Description',
        'Quantite',
        'Utiliser',
        'En_stock',
        'Observation',
        'Commentaire'
    )
    search_fields = ('Description',)