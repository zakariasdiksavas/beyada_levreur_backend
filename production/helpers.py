from .models import Production
from commands.models import Commande


#Create a command once production is entered to a binded batiment
def create_command_from_production(instance:Production, client):
    Commande.objects.create(
        batiment=instance.batiment,
        client=client,
        quantity=instance.normal,
        poids_plateau=instance.poids_plateau,
        pu=0,
        description="Production created",
        is_delivered=False,
        auto_created=True,
        production_source=instance,
        created_by=instance.created_by
    )

#Update a command once production is entered to a binded batiment
def update_command_from_production(instance:Production):
    commande = Commande.objects.filter(production_source=instance, is_delivered=False).last()
    if commande:
        commande.batiment=instance.batiment
        commande.quantity = instance.normal
        commande.poids_plateau = instance.poids_plateau
        commande.save()