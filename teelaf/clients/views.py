import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import ClientIndividuelForm, ClientEntrepriseForm, ClientProspectForm
from .models import ClientIndividuel, ClientEntreprise, ClientProspect
from django.db import models
from django.contrib import messages
import io
import pandas as pd
from datetime import datetime

# Gestion des clients individuels
def manage_clients_individuels(request):
    if request.method == 'POST':
        form = ClientIndividuelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client individuel ajouté avec succès.")
            return redirect('manage_clients_individuels')
    else:
        form = ClientIndividuelForm()
    clients = ClientIndividuel.objects.all().order_by('-date_enregistrement')
    total_count = clients.count()
    satisfaction_counts = clients.values('satisfaction').annotate(count=models.Count('satisfaction'))
    return render(request, 'clients/manage_clients_individuels.html', {
        'form': form,
        'clients': clients,
        'total_count': total_count,
        'satisfaction_counts': satisfaction_counts,
    })

def client_individuel_edit(request, pk):
    client = get_object_or_404(ClientIndividuel, pk=pk)
    if request.method == 'POST':
        form = ClientIndividuelForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client individuel modifié avec succès.")
            return redirect('manage_clients_individuels')
    else:
        form = ClientIndividuelForm(instance=client)
    return render(request, 'clients/client_individuel_edit.html', {'form': form, 'client': client})

def client_individuel_delete(request, pk):
    client = get_object_or_404(ClientIndividuel, pk=pk)
    client.delete()
    messages.success(request, "Client individuel supprimé avec succès.")
    return redirect('manage_clients_individuels')

def clients_individuels_import(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        csv_file = request.FILES['import_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Veuillez sélectionner un fichier CSV valide.")
            return redirect('manage_clients_individuels')
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            count = 0
            doublons = 0
            for row in reader:
                matricule = row.get('Matricule') or row.get('matricule')
                if not matricule:
                    continue
                if ClientIndividuel.objects.filter(matricule=matricule).exists():
                    messages.warning(request, f"Matricule {matricule} déjà existant, ignoré.")
                    doublons += 1
                    continue
                client = ClientIndividuel(
                    matricule=matricule,
                    date_enregistrement = row.get('Date enregistrement') or None,
                    prenoms_nom = row.get('Nom'),
                    contact = row.get('Contact'),
                    email = row.get('Email'),
                    type_service = row.get('Type service'),
                    date_debut = row.get('Date début') or None,
                    date_fin = row.get('Date fin') or None,
                    commentaire = row.get('Commentaire'),
                    satisfaction = row.get('Satisfaction'),
                )
                date_fmt = "%Y-%m-%d"
                for field in ['date_enregistrement', 'date_debut', 'date_fin']:
                    value = getattr(client, field)
                    if value and not isinstance(value, datetime):
                        try:
                            setattr(client, field, datetime.strptime(value, date_fmt).date())
                        except Exception:
                            setattr(client, field, None)
                client.save()
                count += 1
            messages.success(request, f"{count} clients importés avec succès.")
            if doublons:
                messages.info(request, f"{doublons} doublons ignorés.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")
    else:
        messages.error(request, "Aucun fichier importé.")
    return redirect('manage_clients_individuels')

def clients_individuels_export_csv(request):
    clients = ClientIndividuel.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients_individuels.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Matricule', 'Date enregistrement', 'Nom', 'Contact', 'Email',
        'Type service', 'Date début', 'Date fin', 'Commentaire', 'Satisfaction'
    ])
    for client in clients:
        writer.writerow([
            client.matricule, client.date_enregistrement, client.prenoms_nom, client.contact,
            client.email, client.type_service, client.date_debut, client.date_fin,
            client.commentaire, client.satisfaction
        ])
    return response

def clients_individuels_export_excel(request):
    clients = ClientIndividuel.objects.all()
    data = []
    for client in clients:
        data.append({
            'Matricule': client.matricule,
            'Date enregistrement': client.date_enregistrement,
            'Nom': client.prenoms_nom,
            'Contact': client.contact,
            'Email': client.email,
            'Type service': client.type_service,
            'Date début': client.date_debut,
            'Date fin': client.date_fin,
            'Commentaire': client.commentaire,
            'Satisfaction': client.satisfaction,
        })
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Clients Individuels')
    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=clients_individuels.xlsx'
    return response

# Gestion des entreprises
def manage_clients_entreprises(request):
    if request.method == 'POST':
        form = ClientEntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Entreprise ajoutée avec succès.")
            return redirect('manage_clients_entreprises')
    else:
        form = ClientEntrepriseForm()
    entreprises = ClientEntreprise.objects.all().order_by('-id')
    total_count = entreprises.count()
    satisfaction_counts = entreprises.values('satisfaction').annotate(count=models.Count('satisfaction'))
    return render(request, 'clients/manage_clients_entreprises.html', {
        'form': form,
        'entreprises': entreprises,
        'total_count': total_count,
        'satisfaction_counts': satisfaction_counts,
    })

def client_entreprise_edit(request, pk):
    entreprise = get_object_or_404(ClientEntreprise, pk=pk)
    if request.method == 'POST':
        form = ClientEntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, "Entreprise modifiée avec succès.")
            return redirect('manage_clients_entreprises')
    else:
        form = ClientEntrepriseForm(instance=entreprise)
    return render(request, 'clients/client_entreprise_edit.html', {'form': form, 'entreprise': entreprise})

def client_entreprise_delete(request, pk):
    entreprise = get_object_or_404(ClientEntreprise, pk=pk)
    entreprise.delete()
    messages.success(request, "Entreprise supprimée avec succès.")
    return redirect('manage_clients_entreprises')

def clients_entreprises_import(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        csv_file = request.FILES['import_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Veuillez sélectionner un fichier CSV valide.")
            return redirect('manage_clients_entreprises')
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            count = 0
            doublons = 0
            for row in reader:
                matricule = row.get('Matricule') or row.get('matricule')
                if not matricule:
                    continue
                if ClientEntreprise.objects.filter(matricule=matricule).exists():
                    messages.warning(request, f"Matricule {matricule} déjà existant, ignoré.")
                    doublons += 1
                    continue
                entreprise = ClientEntreprise(
                    matricule=matricule,
                    entreprise = row.get('Nom entreprise') or row.get('entreprise'),
                    beneficiaire = row.get('Bénéficiaire') or row.get('beneficiaire'),
                    point_contact = row.get('Point contact') or row.get('point_contact'),
                    numero = row.get('Contact') or row.get('numero'),
                    email = row.get('Email'),
                    type_service = row.get('Type service') or row.get('type_service'),
                    commentaire = row.get('Commentaire'),
                    satisfaction = row.get('Satisfaction'),
                )
                entreprise.save()
                count += 1
            messages.success(request, f"{count} entreprises importées avec succès.")
            if doublons:
                messages.info(request, f"{doublons} doublons ignorés.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")
    else:
        messages.error(request, "Aucun fichier importé.")
    return redirect('manage_clients_entreprises')

def clients_entreprises_export_csv(request):
    entreprises = ClientEntreprise.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients_entreprises.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Matricule', 'Nom entreprise', 'Bénéficiaire', 'Point contact', 'Contact',
        'Email', 'Type service', 'Commentaire', 'Satisfaction'
    ])
    for e in entreprises:
        writer.writerow([
            e.matricule, e.entreprise, e.beneficiaire, e.point_contact, e.numero,
            e.email, e.type_service, e.commentaire, e.satisfaction
        ])
    return response

def clients_entreprises_export_excel(request):
    entreprises = ClientEntreprise.objects.all()
    data = []
    for e in entreprises:
        data.append({
            'Matricule': e.matricule,
            'Nom entreprise': e.entreprise,
            'Bénéficiaire': e.beneficiaire,
            'Point contact': e.point_contact,
            'Contact': e.numero,
            'Email': e.email,
            'Type service': e.type_service,
            'Commentaire': e.commentaire,
            'Satisfaction': e.satisfaction,
        })
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Entreprises')
    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=clients_entreprises.xlsx'
    return response

# Gestion des prospects
def manage_clients_prospects(request):
    if request.method == 'POST':
        form = ClientProspectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Prospect ajouté avec succès.")
            return redirect('manage_clients_prospects')
    else:
        form = ClientProspectForm()
    prospects = ClientProspect.objects.all().order_by('-id')
    total_count = prospects.count()
    return render(request, 'clients/manage_clients_prospects.html', {
        'form': form,
        'prospects': prospects,
        'total_count': total_count,
    })

def client_prospect_edit(request, pk):
    prospect = get_object_or_404(ClientProspect, pk=pk)
    if request.method == 'POST':
        form = ClientProspectForm(request.POST, instance=prospect)
        if form.is_valid():
            form.save()
            messages.success(request, "Prospect modifié avec succès.")
            return redirect('manage_clients_prospects')
    else:
        form = ClientProspectForm(instance=prospect)
    return render(request, 'clients/client_prospect_edit.html', {'form': form, 'prospect': prospect})

def client_prospect_delete(request, pk):
    prospect = get_object_or_404(ClientProspect, pk=pk)
    prospect.delete()
    messages.success(request, "Prospect supprimé avec succès.")
    return redirect('manage_clients_prospects')

def clients_prospects_import(request):
    if request.method == 'POST' and request.FILES.get('import_file'):
        csv_file = request.FILES['import_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Veuillez sélectionner un fichier CSV valide.")
            return redirect('manage_clients_prospects')
        try:
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            count = 0
            doublons = 0
            for row in reader:
                matricule = row.get('Matricule') or row.get('matricule')
                if not matricule:
                    continue
                if ClientProspect.objects.filter(matricule=matricule).exists():
                    messages.warning(request, f"Matricule {matricule} déjà existant, ignoré.")
                    doublons += 1
                    continue
                prospect = ClientProspect(
                    matricule = matricule,
                    date_enregistrement = row.get('Date enregistrement') or None,
                    prenoms_nom = row.get('Nom') or row.get('prenoms_nom'),
                    contact = row.get('Contact'),
                    email = row.get('Email'),
                    point_focal = row.get('Point focal') or row.get('point_focal'),
                    deja_contact = True if (row.get('Déjà contact') or '').strip().lower() in ['oui', 'yes', '1', 'true'] else False,
                    date_dernier_contact = row.get('Date dernier contact') or row.get('date_dernier_contact') or None,
                    commentaire = row.get('Commentaire'),
                )
                date_fmt = "%Y-%m-%d"
                for field in ['date_enregistrement', 'date_dernier_contact']:
                    value = getattr(prospect, field)
                    if value and not isinstance(value, datetime):
                        try:
                            setattr(prospect, field, datetime.strptime(value, date_fmt).date())
                        except Exception:
                            setattr(prospect, field, None)
                prospect.save()
                count += 1
            messages.success(request, f"{count} prospects importés avec succès.")
            if doublons:
                messages.info(request, f"{doublons} doublons ignorés.")
        except Exception as e:
            messages.error(request, f"Erreur lors de l'import : {e}")
    else:
        messages.error(request, "Aucun fichier importé.")
    return redirect('manage_clients_prospects')

def clients_prospects_export_csv(request):
    prospects = ClientProspect.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clients_prospects.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Matricule', 'Date enregistrement', 'Nom', 'Contact', 'Email',
        'Point focal', 'Déjà contact', 'Date dernier contact', 'Commentaire'
    ])
    for prospect in prospects:
        writer.writerow([
            prospect.matricule,
            prospect.date_enregistrement,
            prospect.prenoms_nom,
            prospect.contact,
            prospect.email,
            prospect.point_focal,
            'Oui' if prospect.deja_contact else 'Non',
            prospect.date_dernier_contact,
            prospect.commentaire
        ])
    return response

def clients_prospects_export_excel(request):
    prospects = ClientProspect.objects.all()
    data = []
    for prospect in prospects:
        data.append({
            'Matricule': prospect.matricule,
            'Date enregistrement': prospect.date_enregistrement,
            'Nom': prospect.prenoms_nom,
            'Contact': prospect.contact,
            'Email': prospect.email,
            'Point focal': prospect.point_focal,
            'Déjà contact': 'Oui' if prospect.deja_contact else 'Non',
            'Date dernier contact': prospect.date_dernier_contact,
            'Commentaire': prospect.commentaire,
        })
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Prospects')
    output.seek(0)
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=clients_prospects.xlsx'
    return response