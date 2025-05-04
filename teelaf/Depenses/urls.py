from django.urls import path
from . import views

urlpatterns = [
    path('', views.depenses_main, name='depenses_main'),

    # Import routes (importation de fichiers CSV/Excel)
    path('formations/import/', views.import_formations, name='import_formations'),
    path('depenses/import/', views.import_depenses, name='import_depenses'),

    # Routes pour modification/suppression des dépenses
    path('depense/modifier/<int:pk>/', views.modifier_depense, name='modifier_depense'),
    path('depense/supprimer/<int:pk>/', views.supprimer_depense, name='supprimer_depense'),

    # Routes pour modification/suppression des formations
    path('formation/modifier/<int:pk>/', views.modifier_formation, name='modifier_formation'),
    path('formation/supprimer/<int:pk>/', views.supprimer_formation, name='supprimer_formation'),

    # Route pour les statistiques de formations (optionnel mais recommandé)
    path('formations/statistiques/', views.statistiques_formations, name='statistiques_formations'),
]