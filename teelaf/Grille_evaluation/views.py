import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import GrilleEvaluation, Learner
from .forms import GrilleEvaluationForm

def grille_list(request):
    fields_exclus = [
        'learner', 'moyenne_ponderee', 'point_amelioration',
        'appreciation', 'numero_attestation', 'date_fin_formation', 'attestation'
    ]
    if request.method == 'POST' and 'import_file' not in request.FILES:
        form = GrilleEvaluationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Grille enregistrée avec succès.")
            return redirect('Grille_evaluation:grille_list')
        else:
            messages.error(request, "Erreur lors de l'enregistrement. Vérifiez les champs.")
    else:
        form = GrilleEvaluationForm()

    grilles = GrilleEvaluation.objects.all()
    apprenants = Learner.objects.all()
    return render(request, 'Grille_evaluation/grille_list.html', {
        'form': form,
        'grilles': grilles,
        'apprenants': apprenants,
        'fields_exclus': fields_exclus,
    })

def import_grilles(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        file = request.FILES['import_file']
        try:
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)

            for _, row in df.iterrows():
                learner = Learner.objects.get(student_id=row['Matricule'])
                GrilleEvaluation.objects.create(
                    learner=learner,
                    moyenne_ponderee=row['Moyenne pondérée'],
                    point_amelioration=row.get('Point d’amélioration', ''),
                    appreciation=row.get('Appréciation', ''),
                    numero_attestation=row.get('N° Attestation', ''),
                    date_fin_formation=row['Date de fin de formation'],
                    # attestation à gérer manuellement si besoin
                )
            messages.success(request, "Importation réussie !")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")
    return redirect('Grille_evaluation:grille_list')

def stats_view(request):
    grilles = GrilleEvaluation.objects.all()
    total = grilles.count()
    # Ajoute ici d'autres statistiques si besoin
    return render(request, 'Grille_evaluation/stats.html', {
        'total': total,
        'grilles': grilles,
    })

# --- AJOUT DES VUES ACTIONS ---

def edit_grille(request, id):
    grille = get_object_or_404(GrilleEvaluation, id=id)
    if request.method == 'POST':
        form = GrilleEvaluationForm(request.POST, request.FILES, instance=grille)
        if form.is_valid():
            form.save()
            messages.success(request, "Grille modifiée avec succès.")
            return redirect('Grille_evaluation:grille_list')
        else:
            messages.error(request, "Erreur lors de la modification. Vérifiez les champs.")
    else:
        form = GrilleEvaluationForm(instance=grille)
    return render(request, 'Grille_evaluation/edit_grille.html', {'form': form, 'grille': grille})

def delete_grille(request, id):
    grille = get_object_or_404(GrilleEvaluation, id=id)
    if request.method == 'POST':
        grille.delete()
        messages.success(request, "Grille supprimée avec succès.")
        return redirect('Grille_evaluation:grille_list')
    return render(request, 'Grille_evaluation/confirm_delete.html', {'grille': grille})