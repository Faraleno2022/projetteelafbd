from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from .forms import LearnerForm
from .models import Learner
import pandas as pd
import csv
import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

def manage_learners(request):
    if request.method == 'POST':
        form = LearnerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_learners')
    else:
        form = LearnerForm()
    learners = Learner.objects.all().order_by('-registration_date')

    # Statistiques
    total_count = learners.exclude(student_id__isnull=True).exclude(student_id__exact='').count()
    etudiant_count = learners.filter(statut="Etudiants _ Elèves").count()
    entrepreneur_count = learners.filter(statut="Entrepreneurs").count()
    professionnel_count = learners.filter(statut="Professionnels").count()
    chomage_count = learners.filter(statut="Sans emploi _ Au chômage").count()
    oui_count = learners.filter(observation="Oui").count()
    non_count = learners.filter(observation="Non").count()

    return render(request, 'learners/manage.html', {
        'form': form,
        'learners': learners,
        'total_count': total_count,
        'etudiant_count': etudiant_count,
        'entrepreneur_count': entrepreneur_count,
        'professionnel_count': professionnel_count,
        'chomage_count': chomage_count,
        'oui_count': oui_count,
        'non_count': non_count,
    })

def learner_edit(request, pk):
    learner = get_object_or_404(Learner, pk=pk)
    if request.method == 'POST':
        form = LearnerForm(request.POST, instance=learner)
        if form.is_valid():
            form.save()
            # AJAX: succès = reload tableau
            if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('manage_learners')
    else:
        form = LearnerForm(instance=learner)

    # Si AJAX, on renvoie juste le formulaire partiel pré-rempli
    if request.GET.get('ajax') == '1' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form_html = render_to_string('learners/_edit_form.html', {'form': form})
        if request.method == 'POST':
            return JsonResponse({'success': False, 'form_html': form_html})
        return HttpResponse(form_html)
    # fallback classique
    return redirect('manage_learners')

def learner_delete(request, pk):
    learner = get_object_or_404(Learner, pk=pk)
    learner.delete()
    return redirect('manage_learners')

def learners_export_csv(request):
    learners = Learner.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="learners.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Nom complet', 'Date de naissance', 'Sexe', 'Téléphone', 'Email',
        'Adresse', 'Statut', 'Formation souhaitée', 'ID Apprenant', 'Observation'
    ])
    for learner in learners:
        writer.writerow([
            learner.full_name, learner.birth_date, learner.gender, learner.phone,
            learner.email, learner.address, learner.statut, learner.desired_course,
            learner.student_id, learner.observation
        ])
    return response

def learners_export_pdf(request):
    learners = Learner.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="learners.pdf"'

    # PDF en mode paysage
    p = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)

    y = height - 40
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "Liste des apprenants")
    y -= 30

    # Enlève l'ID Apprenant des headers
    headers = [
        'Nom complet', 'Date de naissance', 'Sexe', 'Téléphone', 'Email',
        'Adresse', 'Statut', 'Formation souhaitée', 'Observation'
    ]
    p.setFont("Helvetica-Bold", 8)
    for i, header in enumerate(headers):
        p.drawString(40 + i * 90, y, header)
    y -= 20

    p.setFont("Helvetica", 8)
    for learner in learners:
        # N'inclus PAS l'ID apprenant ni aucune action
        values = [
            str(learner.full_name), str(learner.birth_date), str(learner.gender), str(learner.phone),
            str(learner.email), str(learner.address), str(learner.statut), str(learner.desired_course),
            str(learner.observation)
        ]
        for i, value in enumerate(values):
            p.drawString(40 + i * 90, y, value[:20])
        y -= 15
        if y < 50:
            p.showPage()
            y = height - 40
    p.save()
    return response

def learners_export_excel(request):
    learners = Learner.objects.all()
    data = []
    for learner in learners:
        data.append({
            'Nom complet': learner.full_name,
            'Date de naissance': learner.birth_date,
            'Sexe': learner.gender,
            'Téléphone': learner.phone,
            'Email': learner.email,
            'Adresse': learner.address,
            'Statut': learner.statut,
            'Formation souhaitée': learner.desired_course,
            'ID Apprenant': learner.student_id,
            'Observation': learner.observation,
        })
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Apprenants')
    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=learners.xlsx'
    return response

# -------- API JSON pour modification HTML/JS --------
def learner_api(request, pk):
    """
    Vue API pour retourner les données d'un apprenant au format JSON.
    Utilisé pour pré-remplir le formulaire de modification HTML/JS.
    """
    learner = get_object_or_404(Learner, pk=pk)
    data = {
        'id': learner.id,
        'full_name': learner.full_name or '',
        'birth_date': learner.birth_date.isoformat() if learner.birth_date else '',
        'gender': learner.gender or '',
        'phone': learner.phone or '',
        'email': learner.email or '',
        'address': learner.address or '',
        'statut': learner.statut or '',
        'desired_course': learner.desired_course or '',
        'observation': learner.observation or '',
    }
    return JsonResponse(data)