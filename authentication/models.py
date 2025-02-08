from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.

class UserExt(models.Model):

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    eleveur = models.ForeignKey('base.Eleveur', related_name='users', on_delete=models.CASCADE, null=True, blank=True)
    sites = models.ManyToManyField('base.Site')
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.user.username
    