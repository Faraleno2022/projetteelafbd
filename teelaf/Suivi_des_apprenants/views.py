import pandas as pd
import csv
from django.core.files.storage import FileSystemStorage
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Count
from django.template.loader import render_to_string
from .models import SuiviApprenant, Learner
from .forms import SuiviApprenantForm

# Liste des suivis + formulaire d'ajout rapide avec infos apprenant dynamiques
def list_suivi(request):
    if request.method == 'POST':
        form = SuiviApprenantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Suivi ajouté avec succès.')
            return redirect('suivi_list')
    else:
        form = SuiviApprenantForm()
    suivis = SuiviApprenant.objects.all()
    apprenants = Learner.objects.all()

    # Préparer les données pour le JS (id, nom_complet, formation)
    apprenants_js = [
        {
            'id': str(a.id),
            'nom_complet': a.full_name,
            'formation': a.desired_course
        }
        for a in apprenants
    ]

    return render(request, 'suvi_des_apprenant/list.html', {
        'suivis': suivis,
        'form': form,
        'apprenants': apprenants_js,
    })

# Ajouter un suivi (formulaire dédié, optionnel)
def add_suivi(request):
    if request.method == 'POST':
        form = SuiviApprenantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Suivi ajouté avec succès.')
            return redirect('suivi_list')
    else:
        form = SuiviApprenantForm()
    return render(request, 'suvi_des_apprenant/form.html', {'form': form, 'title': 'Ajouter un suivi'})

# Modifier un suivi (AJAX pour modal)
def edit_suivi(request, pk):
    suivi = get_object_or_404(SuiviApprenant, pk=pk)
    if request.method == 'POST':
        form = SuiviApprenantForm(request.POST, instance=suivi)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            messages.success(request, 'Suivi modifié avec succès.')
            return redirect('suivi_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('suvi_des_apprenant/_edit_form.html', {'form': form, 'suivi': suivi}, request=request)
                return JsonResponse({'success': False, 'form_html': html})
    else:
        form = SuiviApprenantForm(instance=suivi)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('suvi_des_apprenant/_edit_form.html', {'form': form, 'suivi': suivi}, request=request)
            return JsonResponse({'form_html': html})
    # fallback classique (non AJAX)
    return render(request, 'suvi_des_apprenant/form.html', {'form': form, 'title': 'Modifier le suivi'})

# Supprimer un suivi
def delete_suivi(request, pk):
    suivi = get_object_or_404(SuiviApprenant, pk=pk)
    if request.method == 'POST':
        suivi.delete()
        messages.success(request, 'Suivi supprimé avec succès.')
        return redirect('suivi_list')
    return render(request, 'suvi_des_apprenant/confirm_delete.html', {'suivi': suivi})

# Statistiques / Récapitulatif
def recap_suivi(request):
    stats = (
        SuiviApprenant.objects.values('Commentaire')
        .order_by('Commentaire')
        .annotate(total=Count('Commentaire'))
    )
    return render(request, 'suvi_des_apprenant/recap.html', {'stats': stats})

# Export CSV
def export_csv(request):
    suivis = SuiviApprenant.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=suivi_apprenants.csv'
    writer = csv.writer(response)
    writer.writerow([
        'ID', 'Nom complet', 'Formation', 'Date début', 'Date fin',
        'Poste avant', 'Poste après', 'Dernier contact', 'Commentaire'
    ])
    for s in suivis:
        writer.writerow([
            s.ID_Apprenant.id,
            getattr(s.ID_Apprenant, 'full_name', ''),
            getattr(s.ID_Apprenant, 'desired_course', ''),
            s.Date_debut,
            s.Date_fin,
            s.Poste_avant_teelaf,
            s.Poste_apres_teelaf,
            s.Dernier_contact,
            s.Commentaire
        ])
    return response

# Export Excel
def export_excel(request):
    suivis = SuiviApprenant.objects.all()
    data = []
    for s in suivis:
        data.append({
            'ID': s.ID_Apprenant.id,
            'Nom complet': getattr(s.ID_Apprenant, 'full_name', ''),
            'Formation': getattr(s.ID_Apprenant, 'desired_course', ''),
            'Date début': s.Date_debut,
            'Date fin': s.Date_fin,
            'Poste avant': s.Poste_avant_teelaf,
            'Poste après': s.Poste_apres_teelaf,
            'Dernier contact': s.Dernier_contact,
            'Commentaire': s.Commentaire,
        })
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=suivi_apprenants.xlsx'
    df.to_excel(response, index=False)
    return response

# Export PDF (simple tableau)
def export_pdf(request):
    suivis = SuiviApprenant.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="suivi_apprenants.pdf"'
    p = canvas.Canvas(response)
    y = 800
    p.setFont("Helvetica", 10)
    p.drawString(30, y, "ID | Nom complet | Formation | Date début | Date fin | Poste avant | Poste après | Dernier contact | Commentaire")
    y -= 20
    for s in suivis:
        row = f"{s.ID_Apprenant.id} | {getattr(s.ID_Apprenant, 'full_name', '')} | {getattr(s.ID_Apprenant, 'desired_course', '')} | {s.Date_debut} | {s.Date_fin} | {s.Poste_avant_teelaf} | {s.Poste_apres_teelaf} | {s.Dernier_contact} | {s.Commentaire}"
        p.drawString(30, y, row[:180])  # Limite la largeur
        y -= 20
        if y < 40:
            p.showPage()
            y = 800
    p.save()
    return response

# Import CSV/Excel
def import_suivi(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        file = request.FILES['import_file']
        ext = file.name.split('.')[-1]
        if ext == 'csv':
            df = pd.read_csv(file)
        elif ext in ['xls', 'xlsx']:
            df = pd.read_excel(file)
        else:
            messages.error(request, "Format de fichier non supporté.")
            return redirect('suivi_list')
        for _, row in df.iterrows():
            try:
                learner = Learner.objects.get(id=row['ID'])
                SuiviApprenant.objects.update_or_create(
                    ID_Apprenant=learner,
                    defaults={
                        'Date_debut': row['Date début'],
                        'Date_fin': row['Date fin'],
                        'Poste_avant_teelaf': row['Poste avant'],
                        'Poste_apres_teelaf': row['Poste après'],
                        'Dernier_contact': row['Dernier contact'],
                        'Commentaire': row['Commentaire'],
                    }
                )
            except Exception as e:
                messages.error(request, f"Erreur sur la ligne {row.get('ID', '')}: {e}")
        messages.success(request, "Importation terminée.")
    return redirect('suivi_list')