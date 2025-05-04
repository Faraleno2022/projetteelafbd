from django.urls import path
from . import views

urlpatterns = [
    # Accueil clients : redirige vers la gestion des clients individuels
    path('', views.manage_clients_individuels, name='clients_home'),

    # Gestion des clients individuels
    path('individuels/', views.manage_clients_individuels, name='manage_clients_individuels'),
    path('individuels/ajouter/', views.manage_clients_individuels, name='ajouter_client_individuel'),
    path('individuels/edit/<int:pk>/', views.client_individuel_edit, name='client_individuel_edit'),
    path('individuels/delete/<int:pk>/', views.client_individuel_delete, name='client_individuel_delete'),
    path('individuels/export/csv/', views.clients_individuels_export_csv, name='clients_individuels_export_csv'),
    path('individuels/export/excel/', views.clients_individuels_export_excel, name='clients_individuels_export_excel'),
    # Ligne supprimée : path('individuels/api/<int:pk>/', views.client_individuel_api, name='client_individuel_api'),
    path('individuels/import/', views.clients_individuels_import, name='clients_individuels_import'),

    # Gestion des clients entreprises
    path('entreprises/', views.manage_clients_entreprises, name='manage_clients_entreprises'),
    path('entreprises/ajouter/', views.manage_clients_entreprises, name='ajouter_client_entreprise'),
    path('entreprises/edit/<int:pk>/', views.client_entreprise_edit, name='client_entreprise_edit'),
    path('entreprises/delete/<int:pk>/', views.client_entreprise_delete, name='client_entreprise_delete'),
    path('entreprises/export/csv/', views.clients_entreprises_export_csv, name='clients_entreprises_export_csv'),
    path('entreprises/export/excel/', views.clients_entreprises_export_excel, name='clients_entreprises_export_excel'),
    path('entreprises/import/', views.clients_entreprises_import, name='clients_entreprises_import'),

    # Gestion des prospects
    path('prospects/', views.manage_clients_prospects, name='manage_clients_prospects'),
    path('prospects/ajouter/', views.manage_clients_prospects, name='ajouter_client_prospect'),
    path('prospects/edit/<int:pk>/', views.client_prospect_edit, name='client_prospect_edit'),
    path('prospects/delete/<int:pk>/', views.client_prospect_delete, name='client_prospect_delete'),
    path('prospects/export/csv/', views.clients_prospects_export_csv, name='clients_prospects_export_csv'),
    path('prospects/export/excel/', views.clients_prospects_export_excel, name='clients_prospects_export_excel'),
    path('prospects/import/', views.clients_prospects_import, name='clients_prospects_import'),
]