from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
#from datetime import datetime, date
from django.utils.timezone import now, datetime


class Entite(models.Model):
    codeEntite = models.CharField(max_length=15, unique=True, blank=False)
    libeleEntite = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.libeleEntite


class Agence(models.Model):
    numeroCodique = models.CharField(max_length=15, unique=True, blank=False)
    libeleAgence = models.CharField(max_length=30, blank=False)
    entite = models.ForeignKey(Entite)


    def __str__(self):
        return self.libeleAgence


class Employe(models.Model):
    user = models.OneToOneField(User)
    # date_of_birth = models.DateField(blank=True, null=True)
    matricule = models.CharField(max_length=30)
    agence = models.ForeignKey(Agence)

    def __str__(self):
        return 'Employe pour utilisateur {}'.format(self.user.username)

class EtatMandat(models.Model):
    codeEtat = models.CharField(max_length=15, blank=False, null=False)
    libelleEtat = models.CharField(max_length=25, blank=True)

    def __str__(self):
        return self.libelleEtat

class Mandat(models.Model):
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    matricule = models.CharField(max_length=20, blank=False)
    prenom =  models.CharField(max_length=30, blank=False)
    nom =  models.CharField(max_length=30, blank=False)
    categorie =  models.CharField(max_length=30, blank=False)
    montant =  models.CharField(max_length=30, blank=False)
    secteur = models.CharField(max_length=30, blank=False)
    date_creation = models.DateField(auto_now_add=True)
    date_modification = models.DateField(auto_now=True)
    periode = models.CharField(max_length=50, blank=False)
    etatMandat = models.SmallIntegerField()

    def __str__(self):
        return self.matricule

    # def get_absolute_url(self):
    # 	return reverse('teyco_pdf', args=[self.id])

class Paiement(models.Model):
    #user = models.ForeignKey(Employe.user)
    matricule = models.CharField(max_length=20, blank=False)
    prenom =  models.CharField(max_length=30, blank=False)
    nom =  models.CharField(max_length=30, blank=False)
    categorie =  models.CharField(max_length=30, blank=True)
    montant =  models.CharField(max_length=30, blank=False)
    secteur = models.CharField(max_length=30, blank=True)
    date_paiement = models.DateField(auto_now_add=True)
    agent_payeur = models.ForeignKey(Employe, null=True)
    mandat_paye = models.ForeignKey(Mandat, null=True)
    agence_payeur = models.ForeignKey(Agence, null=True)
    codeEtat_mandat = models.CharField(max_length=15, blank=False, null=True)
    #libeleAgence = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.matricule



