from django.contrib import admin
from .models import *

# Register your models here.
class DirectSaleAdmin(admin.ModelAdmin):
    list_display = ('client', 'batiment', 'quantity')
    

admin.site.register(DirectSale, DirectSaleAdmin)