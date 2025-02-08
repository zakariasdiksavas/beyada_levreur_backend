from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PaiementByCommand)
admin.site.register(PaiementByClient)
admin.site.register(PaimentByDirectSale)
admin.site.register(PaiementProof)