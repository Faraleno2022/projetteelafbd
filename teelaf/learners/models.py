from django.db import models
from django.utils.crypto import get_random_string

class Learner(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre')
    ]
    STATUT_CHOICES = [
        ("Etudiants _ Elèves", "Etudiants _ Elèves"),
        ("Entrepreneurs", "Entrepreneurs"),
        ("Professionnels", "Professionnels"),
        ("Sans emploi _ Au chômage", "Sans emploi _ Au chômage"),
    ]
    OBS_CHOICES = [("Oui", "Oui"), ("Non", "Non")]

    full_name = models.CharField('Nom complet', max_length=100)
    birth_date = models.DateField('Date de naissance')
    gender = models.CharField('Sexe', max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField('Téléphone', max_length=20)
    email = models.EmailField('Email')
    address = models.CharField('Adresse', max_length=255)
    statut = models.CharField('Statut', max_length=30, choices=STATUT_CHOICES, default="Etudiants _ Elèves")
    desired_course = models.CharField('Formation souhaitée', max_length=100)
    observation = models.CharField('Observation', max_length=3, choices=OBS_CHOICES, default="Non")
    student_id = models.CharField('ID Apprenant', max_length=20, unique=True, blank=True, null=True)
    registration_date = models.DateTimeField('Date inscription', auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            prefix = "GEN"
            date_str = self.registration_date.strftime("%Y%m%d") if self.registration_date else ""
            unique_part = get_random_string(length=4, allowed_chars='0123456789')
            self.student_id = f"{prefix}{date_str}{unique_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name