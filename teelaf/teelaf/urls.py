from django.contrib import admin
from django.urls import path, include
from dashboard.views import HomeView, admin_change_password, manage_user_access
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),  # Dashboard comme point d'entrée
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
    path('learners/', include('learners.urls')),
    path('clients/', include('clients.urls')),
    path('Quit', views.quit_view, name='quit'),
    # Utilise le template registration/login.html pour la connexion
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile_view, name='profile'),

    # Applications spécifiques
    path('suivi_des_apprenants/', include('Suivi_des_apprenants.urls')),
    path('Grille_evaluation/', include(('Grille_evaluation.urls', 'Grille_evaluation'), namespace='Grille_evaluation')),
    path('depenses/', include('Depenses.urls')),
    path('Suivi_projects/', include('Suivi_projects.urls')),

    # Changement de mot de passe par l'admin
    path('admin/change-password/<int:user_id>/', admin_change_password, name='admin_change_password'),

    # Gestion des accès utilisateurs par l'admin
    path('users/<int:user_id>/manage-access/', manage_user_access, name='manage_user_access'),
]

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)