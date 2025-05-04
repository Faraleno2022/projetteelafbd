from django.urls import path
from . import views

urlpatterns = [
    path('', views.manage_learners, name='manage_learners'),
    path('edit/<int:pk>/', views.learner_edit, name='learner_edit'),
    path('delete/<int:pk>/', views.learner_delete, name='learner_delete'),
    path('export/csv/', views.learners_export_csv, name='learners_export_csv'),
    path('export/pdf/', views.learners_export_pdf, name='learners_export_pdf'),
    path('export/excel/', views.learners_export_excel, name='learners_export_excel'),
    # --- API JSON pour modification HTML/JS ---
    path('api/<int:pk>/', views.learner_api, name='learner_api'),
]