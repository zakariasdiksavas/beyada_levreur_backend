from django.contrib import admin
from . import models

# Register your models here.

    
class UserExtAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    

admin.site.register(models.UserExt, UserExtAdmin)