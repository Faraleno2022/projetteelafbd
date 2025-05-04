from django.contrib import admin
from .models import ClientIndividuel, ClientEntreprise, ClientProspect

admin.site.register(ClientIndividuel)
admin.site.register(ClientEntreprise)
admin.site.register(ClientProspect)