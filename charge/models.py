from django.db import models
from simple_history.models import HistoricalRecords
from commands.models import Commande


# Create your models here.
class Charge(models.Model):
    commande = models.ForeignKey(Commande, related_name="charges", on_delete=models.CASCADE, db_index=True)
    driver = models.ForeignKey('base.Driver', related_name="deliveries", on_delete=models.CASCADE)
    eggs_produced_at = models.DateField()
    datetime = models.DateTimeField()
    change = models.IntegerField(default=0)
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.datetime