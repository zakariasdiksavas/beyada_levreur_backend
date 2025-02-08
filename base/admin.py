from django.contrib import admin
from . import models


class EleveurAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email')
    

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'eleveur')
    
    
class BatimentAdmin(admin.ModelAdmin):
    list_display = ('name', 'site')
    
    

#REGISTERING MODELS
admin.site.register(models.Eleveur, EleveurAdmin)
admin.site.register(models.Site, SiteAdmin)
admin.site.register(models.Batiment, BatimentAdmin)
admin.site.register(models.ClientBatiment)
admin.site.register(models.Driver)
