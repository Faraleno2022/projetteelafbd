from django.db import models
from learners.models import Learner

class SuiviApprenant(models.Model):
    ID_Apprenant = models.OneToOneField(Learner, on_delete=models.CASCADE, primary_key=True)
    Date_debut = models.DateField()
    Date_fin = models.DateField()
    Poste_avant_teelaf = models.CharField(max_length=255)
    Poste_apres_teelaf = models.CharField(max_length=255)
    Dernier_contact = models.DateField()
    CHOIX_COMMENTAIRE = [
        ('Excellent', 'Excellent'),
        ('Très satisfait', 'Très satisfait'),
        ('Satisfait', 'Satisfait'),
        ('Assez satisfait', 'Assez satisfait'),
        ('Neutre', 'Neutre'),
        ('Moyennement satisfait', 'Moyennement satisfait'),
        ('Peu satisfait', 'Peu satisfait'),
        ('Insatisfait', 'Insatisfait'),
        ('Pas satisfait', 'Pas satisfait'),
        ('Très insatisfait', 'Très insatisfait'),
        ('Mauvais', 'Mauvais'),
        ('Inacceptable', 'Inacceptable'),
    ]
    Commentaire = models.CharField(max_length=30, choices=CHOIX_COMMENTAIRE, default='Neutre')

    def __str__(self):
        return f"{self.ID_Apprenant.id} - {self.Nom_complet} - {self.Formation_suivi}"

    @property
    def Nom_complet(self):
        return self.ID_Apprenant.full_name

    @property
    def Formation_suivi(self):
        return self.ID_Apprenant.desired_course