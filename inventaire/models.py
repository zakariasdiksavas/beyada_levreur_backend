from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.

class Inventaire(models.Model):
    batiment = models.ForeignKey('base.Batiment', on_delete=models.CASCADE, related_name='inventaire_batiment')
    quantity = models.IntegerField(default=0)
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
    is_positive = models.BooleanField(default=False)
    date = models.DateField()
    history = HistoricalRecords()