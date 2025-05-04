from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from Grille_evaluation.models import GrilleEvaluation

def quit_view(request):
    logout(request)
    return redirect('login')  # Redirige vers la page de connexion

def grille_evaluation(request):
    grilles = GrilleEvaluation.objects.all()
    return render(request, 'Grille_evaluation/grille_list.html', {'grilles': grilles})

@login_required
def profile_view(request):
    return render(request, 'profile.html')