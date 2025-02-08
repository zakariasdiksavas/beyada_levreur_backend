from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.
class Production(models.Model):
    batiment = models.ForeignKey('base.Batiment', related_name='productions', on_delete=models.PROTECT)
    normal = models.IntegerField(default=0)
    double_jaune = models.IntegerField(default=0)
    blanc = models.IntegerField(default=0)
    sale = models.IntegerField(default=0)
    casse = models.IntegerField(default=0)
    elimine = models.FloatField(default=0) #Liquide (kg)
    triage = models.IntegerField(default=0)
    poids_plateau = models.FloatField(default=0)
    tare_alveole = models.FloatField(default=70)
    production_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('auth.User', related_name='productions', on_delete=models.PROTECT, null=True, default=None)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.batiment.name} - {self.production_date}"