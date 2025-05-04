from django.db import models

class Depense(models.Model):
    TYPE_CHOICES = [
        ('depense', 'Dépense'),
        ('recette', 'Recette'),
        ('formation', 'Formation'),
        ('autre', 'Autre'),
    ]
    date = models.DateField()
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    solde = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.description}"

class FraisFormation(models.Model):
    prenom_nom = models.CharField(max_length=255)
    date_inscription = models.DateField()
    formation_suivie = models.CharField(max_length=255)
    frais_formation = models.DecimalField(max_digits=10, decimal_places=2)
    inscription = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # <-- Non obligatoire
    avance_payer = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )  # <-- Non obligatoire
    date_fin = models.DateField()

    @property
    def reste_a_payer(self):
        avance = self.avance_payer if self.avance_payer is not None else 0
        return (self.frais_formation or 0) - avance

    @property
    def statut(self):
        return "Clôturé" if self.reste_a_payer <= 0 else f"Reste à payer: {self.reste_a_payer} GNF"

    def __str__(self):
        return self.prenom_nom