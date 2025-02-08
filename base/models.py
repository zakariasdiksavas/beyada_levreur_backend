from django.db import models
from simple_history.models import HistoricalRecords


# Create your models here.

class Eleveur(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    

class Site(models.Model):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    eleveur = models.ForeignKey(Eleveur, on_delete=models.CASCADE)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.name} - {self.eleveur.name}"
    
    
class Batiment(models.Model):

    site = models.ForeignKey(Site, related_name="batiments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.name} - {self.site.eleveur.name} - {self.site.name}"
    
    
class Client(models.Model):

    name = models.CharField(max_length=100)
    eleveur = models.ForeignKey(Eleveur, related_name="clients", on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_passager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    
class Driver(models.Model):

    client = models.ForeignKey(Client, related_name="drivers", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    cin = models.CharField(max_length=20, null=True, blank=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    
class EggLabels(models.Model):

    eleveur = models.ForeignKey(Eleveur, related_name="egg_labels", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
class ClientBatiment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE)
    is_linked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.client.name} - {self.batiment.name}"