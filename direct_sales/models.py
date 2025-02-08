from django.db import models
from simple_history.models import HistoricalRecords



# Create your models here.
class DirectSale(models.Model):
    client = models.ForeignKey('base.Client', on_delete=models.PROTECT)
    batiment = models.ForeignKey('base.Batiment', on_delete=models.PROTECT)
    init_pu = models.FloatField(default=0) # init price
    day_pu = models.FloatField(default=0) # actual day price
    quantity = models.IntegerField(default=0)
    change = models.IntegerField(default=0)
    date = models.DateTimeField(null=True)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.client} - {self.batiment} - {self.init_pu}"