from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import MemberForm
from .models import Member

def register_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('register_member'))
    else:
        form = MemberForm()

    members = Member.objects.all()
    return render(request, 'members/register.html', {'form': form, 'members': members})

def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect(reverse('register_member'))
    else:
        form = MemberForm(instance=member)
    members = Member.objects.all()
    return render(request, 'members/register.html', {'form': form, 'members': members, 'edit_mode': True, 'edit_member_id': member_id})

def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.delete()
        return redirect(reverse('register_member'))
    return render(request, 'members/confirm_delete.html', {'member': member})

class RegistrationSuccessView(TemplateView):
    template_name = 'members/success.html'