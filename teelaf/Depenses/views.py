from django.shortcuts import render, redirect, get_object_or_404
from .models import Depense, FraisFormation
from .forms import DepenseForm, FraisFormationForm
from django.db.models import Sum, F, FloatField, ExpressionWrapper, Q
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib import messages
import json
from collections import defaultdict
import pandas as pd

def depenses_main(request):
    # Gestion des formulaires
    if request.method == 'POST' and 'submit_depense' in request.POST:
        depense_form = DepenseForm(request.POST)
        if depense_form.is_valid():
            depense_form.save()
            return redirect('depenses_main')
    else:
        depense_form = DepenseForm()

    if request.method == 'POST' and 'submit_formation' in request.POST:
        formation_form = FraisFormationForm(request.POST)
        if formation_form.is_valid():
            formation_form.save()
            messages.success(request, "Frais de formation ajouté avec succès.")
            formation_form = FraisFormationForm()  # Réinitialiser le formulaire après succès
        # Pas de redirection ici !
    else:
        formation_form = FraisFormationForm()

    depenses = Depense.objects.all().order_by('-date')
    formations = FraisFormation.objects.all().order_by('-date_inscription')

    # Calculs totaux pour Gestion des Dépenses
    total_depense = depenses.filter(type='depense').aggregate(total=Sum('solde'))['total'] or 0
    total_recette = depenses.filter(type='recette').aggregate(total=Sum('solde'))['total'] or 0
    total_formation = depenses.filter(type='formation').aggregate(total=Sum('solde'))['total'] or 0
    total_autre = depenses.filter(type='autre').aggregate(total=Sum('solde'))['total'] or 0

    # Calculs totaux pour Frais de formation
    total_frais_formation = formations.aggregate(total=Sum('frais_formation'))['total'] or 0
    total_inscription = formations.aggregate(total=Sum('inscription'))['total'] or 0
    total_avance = formations.aggregate(total=Sum('avance_payer'))['total'] or 0
    # Reste à payer = Somme(frais_formation - avance_payer)
    total_reste = formations.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('frais_formation') - F('avance_payer'),
                output_field=FloatField()
            )
        )
    )['total'] or 0

    # ⛔️ NE PAS AJOUTER DE BOUCLE QUI ASSIGNE .reste_a_payer !

    context = {
        'depense_form': depense_form,
        'formation_form': formation_form,
        'depenses': depenses,
        'formations': formations,
        # Totaux Dépenses
        'total_depense': total_depense,
        'total_recette': total_recette,
        'total_formation': total_formation,
        'total_autre': total_autre,
        # Totaux Formations
        'total_frais_formation': total_frais_formation,
        'total_inscription': total_inscription,
        'total_avance': total_avance,
        'total_reste': total_reste,
    }
    return render(request, 'Depenses/depenses_main.html', context)

def statistiques_formations(request):
    formations_qs = FraisFormation.objects.all()
    nb_formations = formations_qs.count()
    total_paye = formations_qs.aggregate(total=Sum('avance_payer'))['total'] or 0
    total_reste = formations_qs.aggregate(
        total=Sum(F('frais_formation') - F('avance_payer'))
    )['total'] or 0

    formations_stats_qs = (
        formations_qs.values('formation_suivie')
        .annotate(
            total_paye=Sum('avance_payer'),
            total_reste=Sum(F('frais_formation') - F('avance_payer'))
        )
        .order_by('formation_suivie')
    )
    formations_labels = [f['formation_suivie'] for f in formations_stats_qs]
    formations_paye = [float(f['total_paye'] or 0) for f in formations_stats_qs]
    formations_reste = [float(f['total_reste'] or 0) for f in formations_stats_qs]

    # Reste à payer par date d'inscription (évolution)
    reste_dict = defaultdict(float)
    for formation in formations_qs:
        date = formation.date_inscription
        if date:
            date_str = date.strftime('%Y-%m-%d')
            reste = float(formation.frais_formation or 0) - float(formation.avance_payer or 0)
            reste_dict[date_str] += reste

    reste_dates = sorted(reste_dict.keys())
    reste_values = [reste_dict[d] for d in reste_dates]

    # Répartition des statuts (clôturé/restant)
    nb_cloture = sum(
        1 for f in formations_qs
        if float(f.frais_formation or 0) - float(f.avance_payer or 0) == 0
    )
    nb_reste = nb_formations - nb_cloture
    statut_labels = ['Clôturé', 'Reste']
    statut_values = [nb_cloture, nb_reste]

    context = {
        'nb_formations': nb_formations,
        'total_paye': total_paye,
        'total_reste': total_reste,
        'formations_labels': mark_safe(json.dumps(formations_labels)),
        'formations_paye': mark_safe(json.dumps(formations_paye)),
        'formations_reste': mark_safe(json.dumps(formations_reste)),
        'reste_dates': mark_safe(json.dumps(reste_dates)),
        'reste_values': mark_safe(json.dumps(reste_values)),
        'statut_labels': mark_safe(json.dumps(statut_labels)),
        'statut_values': mark_safe(json.dumps(statut_values)),
        'montants_par_formation': formations_stats_qs,  # <-- AJOUT pour le tableau du template
    }
    return render(request, 'Depenses/statistiques_formations.html', context)

def import_formations(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        file = request.FILES['import_file']
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            for _, row in df.iterrows():
                FraisFormation.objects.create(
                    prenom_nom=row['prenom_nom'],
                    date_inscription=row['date_inscription'],
                    formation_suivie=row['formation_suivie'],
                    frais_formation=row['frais_formation'],
                    inscription=row['inscription'] if not pd.isna(row['inscription']) else None,
                    avance_payer=row['avance_payer'] if not pd.isna(row['avance_payer']) else None,
                    date_fin=row.get('date_fin', None),
                )
            messages.success(request, "Importation des formations réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")
    return redirect('depenses_main')

def import_depenses(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        file = request.FILES['import_file']
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            for _, row in df.iterrows():
                Depense.objects.create(
                    date=row['date'],
                    description=row['description'],
                    type=row['type'],
                    solde=row['solde'],
                )
            messages.success(request, "Importation des dépenses réussie.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")
    return redirect('depenses_main')

def modifier_depense(request, pk):
    depense = get_object_or_404(Depense, pk=pk)
    if request.method == 'POST':
        form = DepenseForm(request.POST, instance=depense)
        if form.is_valid():
            form.save()
            return redirect('depenses_main')
    else:
        form = DepenseForm(instance=depense)
    return render(request, 'Depenses/modifier_depense.html', {'form': form, 'depense': depense})

def supprimer_depense(request, pk):
    depense = get_object_or_404(Depense, pk=pk)
    if request.method == 'POST':
        depense.delete()
        return redirect('depenses_main')
    return render(request, 'Depenses/supprimer_depense.html', {'depense': depense})

def modifier_formation(request, pk):
    formation = get_object_or_404(FraisFormation, pk=pk)
    if request.method == 'POST':
        form = FraisFormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            return redirect('depenses_main')
    else:
        form = FraisFormationForm(instance=formation)
    return render(request, 'Depenses/modifier_formation.html', {'form': form, 'formation': formation})

def supprimer_formation(request, pk):
    formation = get_object_or_404(FraisFormation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        return redirect('depenses_main')
    return render(request, 'Depenses/supprimer_formation.html', {'formation': formation})