from django.db import models
from simple_history.models import HistoricalRecords
from commands.models import Commande
from base.models import Client
from direct_sales.models import DirectSale



# Create your models here.
class PaiementByCommand(models.Model):
    commande = models.ForeignKey(Commande, related_name="paiements", on_delete=models.PROTECT)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.commande} - {self.amount}"
    
    
class PaiementByClient(models.Model):
    client = models.ForeignKey(Client, related_name='paiements', on_delete=models.PROTECT)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.client} - {self.amount}"
    
    
class PaimentByDirectSale(models.Model):
    direct_sale = models.ForeignKey(DirectSale, related_name='paiements', on_delete=models.PROTECT)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.direct_sale} - {self.amount}"


class PaiementTry(models.Model):
    paiement_by_command = models.ForeignKey(PaiementByCommand, related_name='tries', on_delete=models.CASCADE, null=True)
    paiement_by_client = models.ForeignKey(PaiementByClient, related_name='tries', on_delete=models.CASCADE, null=True)
    paiement_direct_sale = models.ForeignKey(PaimentByDirectSale, related_name='tries', on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True)
    PAIEMENT_MODES = (
        (1, 'Espéce'),
        (2, 'Chèque'),
        (3, 'LCN'),
        (4, 'Virement'),
    )
    amount = models.FloatField(default=0)
    paiement_mode = models.IntegerField(choices=PAIEMENT_MODES, default=1)
    PAYMENT_STATUS = (
        (1, 'en cours'),
        (2, 'payé'),
        (3, 'échec'),
    )
    status = models.IntegerField(choices=PAYMENT_STATUS, default=1)
    date = models.DateField(null=True)
    history = HistoricalRecords()
    
    
class PaiementProof(models.Model):
    paiement_try = models.ForeignKey(PaiementTry, related_name='proofs', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='uploads/paiements/proofs/')
    history = HistoricalRecords()
    
