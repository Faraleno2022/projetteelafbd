from django.db import models

class SuiviProjet(models.Model):
    Titre_et_zone = models.CharField(max_length=255)
    Date_de_début = models.DateField()
    Date_de_fin = models.DateField()
    Budget_alloue = models.DecimalField(max_digits=12, decimal_places=2)
    Depenses_reelles = models.DecimalField(max_digits=12, decimal_places=2)
    Subventions = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    Participants = models.TextField()
    Beneficiaire = models.CharField(max_length=255)
    Statuts = models.CharField(max_length=100)

    def __str__(self):
        return self.Titre_et_zone

class SuiviInventaire(models.Model):
    Description = models.CharField(max_length=255)
    Quantite = models.PositiveIntegerField()
    Utiliser = models.PositiveIntegerField()
    En_stock = models.PositiveIntegerField()
    Observation = models.TextField(blank=True, null=True)
    Commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.Description