from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Solicitante)
class SolicitanteAdmin(admin.ModelAdmin):
	pass
	
	

admin.site.register(Municipio)
admin.site.register(Parroquia)
admin.site.register(Comuna)
