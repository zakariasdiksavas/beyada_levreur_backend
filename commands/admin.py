from django.contrib import admin
from .models import *

# Register your models here.
class CommandAdmin(admin.ModelAdmin):
    list_display = ('client', 'batiment')
    

admin.site.register(Commande, CommandAdmin)
