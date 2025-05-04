from django.urls import path
from . import views

urlpatterns = [
    # Vue principale
    path('', views.suivi_projects_main, name='suivi_projects_main'),

    # Routes pour modification/suppression des projets
    path('projet/modifier/<int:pk>/', views.modifier_projet, name='modifier_projet'),
    path('projet/supprimer/<int:pk>/', views.supprimer_projet, name='supprimer_projet'),

    # Routes pour modification/suppression des inventaires
    path('inventaire/modifier/<int:pk>/', views.modifier_inventaire, name='modifier_inventaire'),
    path('inventaire/supprimer/<int:pk>/', views.supprimer_inventaire, name='supprimer_inventaire'),

    # (Optionnel) Ajoute ici d'autres routes si besoin, comme des imports ou statistiques
]