from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Production
from commands.models import Commande
from base.models import ClientBatiment
from .helpers import *


#create commande when production is created
@receiver(post_save, sender=Production)
def production_created_handler(sender, instance: Production, created, **kwargs):
    if created:
        
        #Create a command once production is entered to a binded batiment
        batiment_binded = ClientBatiment.objects.filter(batiment=instance.batiment).only("is_linked", "client").order_by("created_at").last()
        if batiment_binded and batiment_binded.is_linked:
            create_command_from_production(instance, batiment_binded.client)

    else:
        #Update a command once production is entered to a binded batiment
        update_command_from_production(instance)
        
            

#delete commande when production is deleted
@receiver(post_delete, sender=Production)
def handle_model_delete(sender, instance, **kwargs):
    commande = Commande.objects.filter(production_source=instance).last()
    if commande:
        commande.delete()