from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


# Create your models here.
class Commande(models.Model):
    batiment = models.ForeignKey('base.Batiment', related_name='commands', on_delete=models.PROTECT, db_index=True)
    client = models.ForeignKey('base.Client', related_name='commands', on_delete=models.PROTECT, db_index=True)
    created_by = models.ForeignKey('auth.User', related_name='commands', on_delete=models.PROTECT, null=True, default=None)
    quantity = models.IntegerField(default=0, null=False, blank=False)
    poids_plateau = models.FloatField(default=0, null=False, blank=False)
    pu = models.FloatField(default=0, null=False, blank=False)
    description = models.CharField(max_length=200)
    is_delivered = models.BooleanField(default=False)
    auto_created = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)
    CLASSES = (
        (1, "normal"),
        (2, "double jaune"),
        (3, "blanc"),
        (4, "sale"),
        (5, "casse"),
        (6, "elimine"),
        (7, "triage"),
    )
    classe = models.IntegerField(choices=CLASSES, default=1)
    production_source = models.OneToOneField('production.Production', related_name='commands', on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.client.name} - {self.batiment.name} - {self.quantity} - {self.pu}"