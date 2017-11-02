from django.contrib import admin
from .models import Entite, Agence, Employe, EtatMandat, Mandat, Paiement
# Register your models here.
class MandatAdmin(admin.ModelAdmin):
    # class Meta:
    # 	model = Teyco
    search_fields = ('prenom', 'nom', 'matricule')
    # list_display = ['code', 'prenom', 'nom', 'categorie', 'montant', teyco_pdf]
    list_display = ['matricule', 'prenom', 'nom', 'categorie', 'montant','etatMandat']
    list_filter = ('periode', 'etatMandat')  # actions = [export_to_csv]

class PaiementAdmin(admin.ModelAdmin):
    # class Meta:
    # 	model = Teyco
    search_fields = ('prenom', 'nom', 'matricule')
    # list_display = ['code', 'prenom', 'nom', 'categorie', 'montant', teyco_pdf]
    list_display = ['matricule', 'prenom', 'nom', 'categorie', 'montant','agence_payeur','codeEtat_mandat','date_paiement']
    list_filter = ('codeEtat_mandat',)  # actions = [export_to_csv]



admin.site.register(Mandat, MandatAdmin)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(Entite)
admin.site.register(Agence)
admin.site.register(Employe)
admin.site.register(EtatMandat)
#admin.site.register(Paiement)
