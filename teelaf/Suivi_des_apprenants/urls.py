from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_suivi, name='suivi_list'),
    path('ajouter/', views.add_suivi, name='suivi_add'),
    path('modifier/<int:pk>/', views.edit_suivi, name='suivi_edit'),
    path('supprimer/<int:pk>/', views.delete_suivi, name='suivi_delete'),
    path('export/csv/', views.export_csv, name='suivi_export_csv'),
    path('export/excel/', views.export_excel, name='suivi_export_excel'),
    path('export/pdf/', views.export_pdf, name='suivi_export_pdf'),
    path('import/', views.import_suivi, name='suivi_import'),
    path('recap/', views.recap_suivi, name='suivi_recap'),
]