from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import Fenetre, UserAccess

from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_superuser:
            # L’admin voit tout
            context['fenetres'] = Fenetre.objects.all()
            context['is_admin'] = True
        else:
            # Les autres voient seulement leurs accès
            context['fenetres'] = Fenetre.objects.filter(useraccess__user=user)
            context['is_admin'] = False

        return context

@user_passes_test(lambda u: u.is_superuser)
def admin_change_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('user_detail', kwargs={'user_id': user.id}))
    else:
        form = SetPasswordForm(user)
    return render(request, 'dashboard/admin_change_password.html', {'form': form, 'target_user': user})

@login_required
def user_list(request):
    users = User.objects.all()
    is_admin = request.user.is_superuser
    return render(request, 'dashboard/user_list.html', {'users': users, 'is_admin': is_admin})

@login_required
def user_detail(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    is_admin = request.user.is_superuser
    return render(request, 'dashboard/user_detail.html', {'target_user': target_user, 'is_admin': is_admin})

# ---- NOUVELLE VUE POUR GÉRER LES ACCÈS UTILISATEUR ----

@user_passes_test(lambda u: u.is_superuser)
def manage_user_access(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    all_fenetres = Fenetre.objects.all()
    user_fenetres = Fenetre.objects.filter(useraccess__user=user)

    if request.method == 'POST':
        selected_fenetres = request.POST.getlist('fenetres')
        # Supprimer tous les accès existants
        UserAccess.objects.filter(user=user).delete()
        # Ajouter les nouveaux accès
        for fenetre_id in selected_fenetres:
            fenetre = Fenetre.objects.get(id=fenetre_id)
            UserAccess.objects.create(user=user, fenetre=fenetre)
        return redirect('user_detail', user_id=user.id)

    return render(request, 'dashboard/manage_user_access.html', {
        'target_user': user,
        'all_fenetres': all_fenetres,
        'user_fenetres': user_fenetres
    })