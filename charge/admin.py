from django.contrib import admin
from .models import *

# Register your models here.
class ChargeAdmin(admin.ModelAdmin):
    list_display = ('commande', 'driver', 'datetime', 'change')
    

admin.site.register(Charge, ChargeAdmin)