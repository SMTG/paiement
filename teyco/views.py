import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render
from django.utils.timezone import now, datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import weasyprint
from datetime import date, datetime

from .models import Mandat, Paiement, Employe, Agence
# Create your views here.
def home(request):
    context = {}
    return render(request, 'teyco/home.html', context)

@staff_member_required
def charger_mandat(request):
    if request.POST and request.FILES:
        fichier = request.FILES['csv_file']

        for l in fichier:
            #print(l)
            tab_ligne = l.decode().split(';')
            matricule = str(tab_ligne[1]).strip()
            #print(code)
            prenom = tab_ligne[2].strip()
            nom = tab_ligne[3].strip()
            categorie = tab_ligne[4].strip()
            #montant = print("{:,}".format(tab_ligne[5].strip()).replace(',', ' '))
            montant = tab_ligne[5].strip()
            secteur = tab_ligne[6].strip()
            #periode = tab_ligne[7].strip()
            periode = datetime.now().strftime('%B')+'_'+ str(datetime.now().year) #.strftime('%B')
            etatMandat = 1
            mandat = Mandat.objects.get_or_create(matricule=matricule, prenom=prenom, nom=nom, categorie=categorie, montant=montant, secteur=secteur, periode=periode,etatMandat=int(etatMandat))[0]
            mandat.save()
        messages.success(request, "Fichier charger avec succés")
            #creation_teyco(code, prenom, nom,categorie,montant, secteur)
    return render(request, 'teyco/charger_mandat.html')

def search(request):
    #if 'q' in request.GET and request.GET['q'].strip():
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        # if not q:
        #     error = True
        # else:
        mandat = Mandat.objects.filter(matricule=q, etatMandat=1)
        # try:
        #     teyco = Teyco.objects.get(code=q)
        # except Teyco.DoesNotExist:
        #     teyco=None
        return render(request, 'teyco/search_results.html', {'mandat': mandat, 'query': q})
    else:
        return render(request, 'teyco/search_form.html', {'error': True})


def mandat_pdf(request, id, user_id):
    mandat = get_object_or_404(Mandat, id=id)

    matricule = mandat.matricule
    prenom = mandat.prenom
    nom = mandat.nom
    categorie = mandat.categorie
    montant = mandat.montant
    secteur = mandat.secteur
    #periode = mandat.periode
    #agent_payeur =  get_object_or_404(Employe, user=user.request.id)
    #agent_payeur = Employe.objects.get(user=request.user)
    user = get_object_or_404(User, pk=user_id)
    agent_payeur = Employe.objects.get(user=user)
    mandat_paye = mandat
    agence_payeur = agent_payeur.agence
    #print(agence_payeur)
    codeEtat_mandat = 'TEY001'
    paiement = Paiement.objects.get_or_create(matricule=matricule, prenom=prenom, nom=nom, categorie=categorie, montant=montant,
                                 secteur=secteur, agent_payeur=agent_payeur,mandat_paye=mandat_paye,
                                              agence_payeur=agence_payeur,codeEtat_mandat=codeEtat_mandat)[0]
    paiement.save()
    mandat.etatMandat=2
    mandat.save()
    context ={'mandat': mandat, 'agence_payeur': agence_payeur, 'agent_payeur': agent_payeur}

    html = render_to_string('teyco/mandat_recu.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="allo.pdf"'
    weasyprint.HTML(string=html).write_pdf(response)
    return response

def rapport_jour_pdf(request,user_id):
    username = request.user.username
    user = get_object_or_404(User, pk=user_id)
    agent_payeur = Employe.objects.get(user=user)
    paiements = Paiement.objects.filter(date_paiement=date.today(), agent_payeur=agent_payeur)
    #paiements = Paiement.objects.filter(date_paiement=date.today(),agent_payeur=request.user.id)

    total = 0
    nombre = 0
    for paie in paiements:
        strmon = "".join(paie.montant.split())
        total = total+int(strmon)
        nombre=nombre+1

    total = '{0:,}'.format(total)
    total = total.replace(',', '.')

    context = {'paiements': paiements,'username': username, 'total': total, 'nombre': nombre}
    html = render_to_string('teyco/mandat_rapport_jour.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    weasyprint.HTML(string=html).write_pdf(response)
    return response


def rapport_periodique(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    agent_payeur = Employe.objects.get(user=user)
    error = False
    if 'q1' and 'q2'in request.GET:
        q1 = request.GET['q1']
        q2 = request.GET['q2']
        if not q1:
            error = True
        elif not q2:
            error = True
        else:

            paiement = Paiement.objects.filter(date_paiement__range=(q1,q2), agent_payeur=agent_payeur)
            total = 0
            nombre = 0
            for paie in paiement:
                strmon = "".join(paie.montant.split())
                total = total + int(strmon)
                nombre = nombre + 1

            total = '{0:,}'.format(total)
            total = total.replace(',', '.')

            context = {'paiement': paiement, 'user': user , 'total': total, 'nombre': nombre, 'debut':q1, 'fin': q2}
            html = render_to_string('teyco/search_results_periode.html', context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="report_periode.pdf"'
            weasyprint.HTML(string=html).write_pdf(response)
            return response
            #return render(request, 'teyco/search_results_periode.html', context)

    return render(request, 'teyco/search_form_periodique.html', {'error': error})

def recherche_periodique(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    agent_payeur = Employe.objects.get(user=user)
    error = False
    if 'q1' and 'q2'in request.GET:
        q1 = request.GET['q1']
        q2 = request.GET['q2']
        if not q1:
            error = True
        elif not q2:
            error = True
        else:

            paiement = Paiement.objects.filter(date_paiement__range=(q1,q2), agent_payeur=agent_payeur)
            total = 0
            nombre = 0
            for paie in paiement:
                strmon = "".join(paie.montant.split())
                total = total + int(strmon)
                nombre = nombre + 1

            total = '{0:,}'.format(total)
            total = total.replace(',', '.')

            context = {'paiement': paiement, 'user': user , 'total': total, 'nombre': nombre}
            return render(request, 'teyco/search_results_periode.html', context)

    return render(request, 'teyco/search_form_periodique.html', {'error': error})
