from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('main/', views.index, name="index"),
    path('authentifier/', views.authentifier, name="authentifier"),
    path('pageAjouterCompte/', views.pageAjouterCompte, name="pageAjouterCompte"),
    path('ajouterCompte/', views.ajouterCompte, name="ajouterCompte"),
    path('seDeconnecter/', views.seDeconnecter, name="seDeconnecter"),
    path('listeClasses/', views.listeClasses, name="listeClasses"),
    path('gestionMatiere/', views.gestionMatiere, name="gestionMatiere"),
    path('ajouterMatiere/', views.ajouterMatiere, name="ajouterMatiere"),
    path('supprimerMatiere/<int:id>/', views.supprimerMatiere, name="supprimerMatiere"),
    path('mettreAjourMatiere/<int:id>/', views.mettreAjourMatiere, name="mettreAjourMatiere"),
    path('voirBulletin/<int:classeID>/', views.voirBulletin, name="voirBulletin"),
    path('gestionNoteEtudiant/', views.gestionNoteEtudiant, name="gestionNoteEtudiant"),
    path('modifierNoteEtudiant/', views.modifierNoteEtudiant, name="modifierNoteEtudiant"),
    path('mettreAjourNote/<int:etudiantID>/', views.mettreAjourNote, name="mettreAjourNote"),
]