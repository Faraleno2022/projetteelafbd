from django.db import models
from django.contrib.auth.models import User

class Fenetre(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fenetre = models.ForeignKey(Fenetre, on_delete=models.CASCADE)