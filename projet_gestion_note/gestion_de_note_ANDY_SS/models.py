from django.db import models

class Prof(models.Model):
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    mdp=models.CharField(max_length=100, default="mdp123")

class Classe(models.Model):
    niveau=models.CharField(max_length=100)
    filiere=models.CharField(max_length=100)
    groupe=models.IntegerField()

class Matiere(models.Model):
    profID=models.ForeignKey(Prof, on_delete=models.CASCADE)
    classeID=models.ForeignKey(Classe, on_delete=models.CASCADE)
    libelle=models.CharField(max_length=100)

class Etudiant(models.Model):
    classeID=models.ForeignKey(Classe, on_delete=models.CASCADE)
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    mdp=models.CharField(max_length=100, default="123")

class Note_etudiant(models.Model):
    etudiantID = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    matiereID = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    note = models.IntegerField(default=0)