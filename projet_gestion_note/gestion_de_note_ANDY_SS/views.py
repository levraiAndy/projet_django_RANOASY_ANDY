from django.shortcuts import redirect, render
from .models import Prof, Classe, Matiere, Etudiant, Note_etudiant

import json
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize
from django.db import connection
from django.urls import reverse

def index(request):
    if 'utilisateur' in request.session and 'role' in request.session:
        classeID = ""
        if request.session['role'] == "etudiant":
            classeID=Etudiant.objects.filter(id=request.session['id']).values_list('classeID_id',flat=True)[0]
            # print(classeID)
        return render(request, 'index.html', {'classeID':classeID})
    return render(request, 'login.html')

def login(request):
    if 'utilisateur' in request.session and 'role' in request.session:
        return redirect(index)
    return render(request, 'login.html')

def authentifier(request):
    if 'utilisateur' in request.session and 'role' in request.session:
        return redirect(index)
    if request.method == 'POST':
        v=request.POST['nom']
        w=request.POST['prenom']
        x=request.POST['mdp']
        y=request.POST['type']

        if y == 'prof':
            utilisateur_exist = Prof.objects.filter(nom=v,prenom=w, mdp=x).exists()
            id_ = Prof.objects.filter(nom=v,prenom=w, mdp=x).values_list('id',flat=True)
        if y == 'etudiant':
            utilisateur_exist = Etudiant.objects.filter(nom=v,prenom=w, mdp=x).exists()
            id_ = Etudiant.objects.filter(nom=v,prenom=w, mdp=x).values_list('id',flat=True)

        if utilisateur_exist:
            request.session['id'] = id_[0]
            request.session['utilisateur'] = f"{v} {w}"
            request.session['role'] = y
            # return render(request, 'index.html', {'nom': f"{v} {w}. Rôle: {y}"})
            return redirect(index)
        return render(request, 'login.html', {'exist': 'nope'})

        ################################TEST##############################################
        # pr = Prof.objects.all()
        # et = Etudiant.objects.get(id=1)
        # with connection.cursor() as cursor:
        #     cursor.execute(f"SELECT * FROM gestion_de_note_ANDY_SS_prof WHERE nom = '{v}' AND mdp = '{x}'")#AND prenom = '{w}'
        #     get_wh = cursor.fetchall()

        # serialized_ = serialize('json', pr)
        # serialized__ = serialize('json', [et,])
        # # res = serialize('json',get_wh)
        # #return JsonResponse(serialized_,safe=False)

        # data = {'nom': f"{v} {w}", 'utilisateur_exist':utilisateur_exist, 'mdp':x, 'type':y,'pr':get_wh}
        
        # print(json.dumps(data, indent=4))
        # return JsonResponse(data)
        ##################################FIN##############################################

    return render(request, 'login.html')

def pageAjouterCompte(request):
    cla=Classe.objects.all()
    return render(request, 'creerCompte.html', {'classe':cla})

def ajouterCompte(request):
    v=request.POST['nom']
    w=request.POST['prenom']
    x=request.POST['mdp']
    y=request.POST['type']

    classe = Classe.objects.get(id=request.POST['classe'])

    if y == 'prof':
        prof = Prof(nom=v, prenom=w, mdp=x)
        prof.save()
    if y == 'etudiant':
        et = Etudiant(nom=v, prenom=w, mdp=x, classeID=classe)
        et.save()
    return render(request, 'login.html')

def seDeconnecter(request):
    if 'utilisateur' in request.session and 'role' in request.session:
        request.session.flush()
    return redirect(authentifier)

def listeClasses(request):
    cla=Classe.objects.all()
    et=Etudiant.objects.all()
    return render(request, 'listeClasse.html', {'classe':cla,'etudiant':et,'classeID':Etudiant.objects.filter(id=request.session['id']).values_list('classeID_id',flat=True)[0]})

def ajouterClasse(request):
    v=request.POST['niveau']
    w=request.POST['filiere']
    x=request.POST['groupe']

    classe = Classe(niveau=v, filiere=w, groupe=x)
    classe.save()
    # return render(request, 'listeClasse.html')
    #print(json.dumps({"data":1}, indent=4))

def gestionMatiere(request,message=""):
    if 'id' in request.session and request.session['role'] == "prof":
        et=Etudiant.objects.all()
        cla=Classe.objects.all()
        mat=Matiere.objects.filter(profID_id=request.session['id'])
        return render(request, 'gestionMatiere.html', {'etudiant':et, 'classe':cla, 'matiere':mat,'message':message})
    else:
        return redirect(index)

def ajouterMatiere(request):
    if 'id' in request.session and request.session['role'] == "prof":
        v=request.POST['libelle']
        w=request.POST['classeID']

        cla=Classe.objects.get(id=w)
        prof=Prof.objects.get(id=request.session['id'])

        mat = Matiere(libelle=v, classeID=cla, profID=prof)
        mat.save()
        return redirect(gestionMatiere)
    else:
        return redirect(gestionMatiere)

def supprimerMatiere(request,id):
    mat=Matiere.objects.get(id=id)
    mat.delete()
    return redirect(gestionMatiere)

def mettreAjourMatiere(request, id):
    x=request.POST['libelle']
    cla=Classe.objects.get(id=request.POST['classeID'])
    prof=Prof.objects.get(id=request.session['id'])

    mat=Matiere.objects.get(id=id)
    mat.libelle=x
    mat.classeID=cla
    mat.profID=prof
    mat.save()
    # return redirect(reverse('gestionMatiere', args=("mis_a_jour",)))
    # return redirect(gestionMatiere)
    et=Etudiant.objects.all()
    cla=Classe.objects.all()
    mat=Matiere.objects.filter(profID_id=request.session['id'])
    return render(request, 'gestionMatiere.html', {'etudiant':et, 'classe':cla, 'matiere':mat,'message':"mis_a_jour"})

def voirBulletin(request,classeID):
    if classeID == Etudiant.objects.filter(id=request.session['id']).values_list('classeID_id',flat=True)[0]:
        cla=Classe.objects.get(id=classeID)
        mat=Matiere.objects.filter(classeID=cla)
        matAll=Matiere.objects.all()
        moyenne = 0

        for x in mat:
            note, cree=Note_etudiant.objects.get_or_create(etudiantID_id=request.session['id'],matiereID=x)
            moyenne += note.note

        length_ = Note_etudiant.objects.filter(etudiantID_id=request.session['id']).count()
        noteAll=Note_etudiant.objects.filter(etudiantID_id=request.session['id'])
        moyenne /= length_
        if moyenne < 10:
            mention = "Ajourné !"
        elif moyenne < 12:
            mention = "Passable !"
        elif moyenne < 14:
            mention = "Assès bien !"
        elif moyenne < 16:
            mention = "Bien !"
        else:
            mention = "très bien !"
        return render(request, 'bulletin.html', {'matiere':matAll, 'note':noteAll, 'moyenne':moyenne, 'mention':mention,'classeID':Etudiant.objects.filter(id=request.session['id']).values_list('classeID_id',flat=True)[0]})
    else:
        return redirect(index)
    
def gestionNoteEtudiant(request):
    et=Etudiant.objects.all()
    cla=Classe.objects.all()
    mat=Matiere.objects.all()
    note=Note_etudiant.objects.all()
    return render(request, 'gestionNoteEtudiant.html', {'etudiant':et, 'classe':cla, 'matiere':mat, 'note':note})

def modifierNoteEtudiant(request,etudiantID):
    noteAll=Note_etudiant.objects.filter(etudiantID_id=etudiantID)
    return render(request, 'modifierNoteEtudiant.html', {'note':noteAll})

def mettreAjourNote(request,etudiantID):
    classeID=Etudiant.objects.filter(id=etudiantID).values_list('classeID_id',flat=True)[0]
    # mat=Matiere.objects.filter(classeID_id=classeID)
    for key, val in request.POST.items():
        if not key == 'csrfmiddlewaretoken':
            note=Note_etudiant.objects.get(etudiantID_id=etudiantID, matiereID_id=key)
            note.note = val
            note.save()
            #print(f"k: {key}, v: {val}")
    #return JsonResponse("Reponse: OK",safe=False)
    et=Etudiant.objects.all()
    cla=Classe.objects.all()
    mat=Matiere.objects.all()
    note=Note_etudiant.objects.all()
    return render(request, 'gestionNoteEtudiant.html', {'etudiant':et, 'classe':cla, 'matiere':mat, 'note':note, 'mise_a_jour':'OK'})