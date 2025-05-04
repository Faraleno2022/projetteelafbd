from django.shortcuts import render, redirect, get_object_or_404
from .models import SuiviProjet, SuiviInventaire
from .forms import SuiviProjetForm, SuiviInventaireForm
from django.db.models import Sum
from django.contrib import messages

def suivi_projects_main(request):
    # Initialisation des formulaires
    projet_form = SuiviProjetForm()
    inventaire_form = SuiviInventaireForm()

    # Gestion des soumissions
    if request.method == 'POST':
        if 'submit_projet' in request.POST:
            projet_form = SuiviProjetForm(request.POST)
            inventaire_form = SuiviInventaireForm()
            if projet_form.is_valid():
                projet_form.save()
                messages.success(request, "Projet ajouté avec succès.")
                return redirect('suivi_projects_main')
        elif 'submit_inventaire' in request.POST:
            inventaire_form = SuiviInventaireForm(request.POST)
            projet_form = SuiviProjetForm()
            if inventaire_form.is_valid():
                inventaire_form.save()
                messages.success(request, "Inventaire ajouté avec succès.")
                return redirect('suivi_projects_main')

    projets = SuiviProjet.objects.all().order_by('-Date_de_début')
    inventaires = SuiviInventaire.objects.all().order_by('-id')

    # Calculs totaux pour les projets
    total_budget = projets.aggregate(total=Sum('Budget_alloue'))['total'] or 0
    total_depenses = projets.aggregate(total=Sum('Depenses_reelles'))['total'] or 0
    total_subventions = projets.aggregate(total=Sum('Subventions'))['total'] or 0

    context = {
        'projet_form': projet_form,
        'inventaire_form': inventaire_form,
        'projets': projets,
        'inventaires': inventaires,
        'total_budget': total_budget,
        'total_depenses': total_depenses,
        'total_subventions': total_subventions,
    }
    return render(request, 'Suivi_projects/suivi_projects_main.html', context)

# --- Vues de modification et suppression ---

def modifier_projet(request, pk):
    projet = get_object_or_404(SuiviProjet, pk=pk)
    if request.method == 'POST':
        form = SuiviProjetForm(request.POST, instance=projet)
        if form.is_valid():
            form.save()
            messages.success(request, "Projet modifié avec succès.")
            return redirect('suivi_projects_main')
    else:
        form = SuiviProjetForm(instance=projet)
    return render(request, 'Suivi_projects/modifier_projet.html', {'form': form, 'projet': projet})

def supprimer_projet(request, pk):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        projet = SuiviProjet.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, "Le projet demandé n'existe plus ou a déjà été supprimé.")
        return redirect('suivi_projects_main')
    if request.method == 'POST':
        projet.delete()
        messages.success(request, "Projet supprimé avec succès.")
        return redirect('suivi_projects_main')
    return render(request, 'Suivi_projects/supprimer_projet.html', {'projet': projet})

def modifier_inventaire(request, pk):
    inventaire = get_object_or_404(SuiviInventaire, pk=pk)
    if request.method == 'POST':
        form = SuiviInventaireForm(request.POST, instance=inventaire)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventaire modifié avec succès.")
            return redirect('suivi_projects_main')
    else:
        form = SuiviInventaireForm(instance=inventaire)
    return render(request, 'Suivi_projects/modifier_inventaire.html', {'form': form, 'inventaire': inventaire})

def supprimer_inventaire(request, pk):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        inventaire = SuiviInventaire.objects.get(pk=pk)
    except ObjectDoesNotExist:
        messages.error(request, "L'inventaire demandé n'existe plus ou a déjà été supprimé.")
        return redirect('suivi_projects_main')
    if request.method == 'POST':
        inventaire.delete()
        messages.success(request, "Inventaire supprimé avec succès.")
        return redirect('suivi_projects_main')
    return render(request, 'Suivi_projects/supprimer_inventaire.html', {'inventaire': inventaire})