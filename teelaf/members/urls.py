from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_member, name='register_member'),
    path('edit/<int:member_id>/', views.edit_member, name='member_edit'),
    path('delete/<int:member_id>/', views.delete_member, name='member_delete'),
    path('success/', views.RegistrationSuccessView.as_view(), name='registration_success'),
]