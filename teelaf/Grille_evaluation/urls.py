from django.urls import path
from .views import grille_list, import_grilles, stats_view, edit_grille, delete_grille

urlpatterns = [
    path('', grille_list, name='grille_list'),
    path('import/', import_grilles, name='import_grilles'),
    path('stats/', stats_view, name='stats'),
    path('edit/<int:id>/', edit_grille, name='edit_grille'),
    path('delete/<int:id>/', delete_grille, name='delete_grille'),
]