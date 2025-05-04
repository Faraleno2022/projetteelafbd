from django.db import models
from learners.models import Learner

class GrilleEvaluation(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, verbose_name="Matricule")
    moyenne_ponderee = models.FloatField("Moyenne pondérée")
    point_amelioration = models.CharField("Point d'amélioration", max_length=255, blank=False, null=False)
    appreciation = models.CharField("Appréciation", max_length=255, blank=False, null=False)
    numero_attestation = models.CharField("N° Attestation", max_length=50, blank=True)
    date_fin_formation = models.DateField("Date de fin de formation")
    attestation = models.FileField("Joindre Attestation", upload_to="attestations/", blank=True, null=True)

    def __str__(self):
        return f"{self.learner} - {self.moyenne_ponderee}"