from django.db import models

class ClientIndividuel(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    date_enregistrement = models.DateField(blank=True, null=True)
    prenoms_nom = models.CharField(max_length=150)
    contact = models.CharField(max_length=50)
    email = models.EmailField()
    type_service = models.CharField(max_length=100)
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)
    commentaire = models.TextField(blank=True)
    satisfaction = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.matricule} - {self.prenoms_nom}"

class ClientEntreprise(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    entreprise = models.CharField(max_length=150)
    type_service = models.CharField(max_length=100)
    beneficiaire = models.CharField(max_length=150)
    point_contact = models.CharField(max_length=100)
    numero = models.CharField(max_length=50)
    email = models.EmailField()
    satisfaction = models.CharField(max_length=50)
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return f"{self.matricule} - {self.entreprise}"

class ClientProspect(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    date_enregistrement = models.DateField(blank=True, null=True)
    prenoms_nom = models.CharField(max_length=150)
    point_focal = models.CharField(max_length=100)
    deja_contact = models.BooleanField(default=False)
    email = models.EmailField()
    contact = models.CharField(max_length=50)
    date_dernier_contact = models.DateField(blank=True, null=True)
    commentaire = models.TextField(blank=True)

    def __str__(self):
        return f"{self.matricule} - {self.prenoms_nom}"