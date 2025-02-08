from .models import PaiementTry
from commands.models import Commande
from django.db.models import F, Sum, Case, When, IntegerField



def get_client_command_paiements(client)->dict:
    command_paiements = PaiementTry.objects.filter(client=client, paiement_by_command__isnull=False).aggregate(
        amount_status_1=Sum(
            Case(
                When(status=1, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        ),
        amount_status_2=Sum(
            Case(
                When(status=2, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        ),
        amount_status_3=Sum(
            Case(
                When(status=3, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        )
    )
    return command_paiements


def get_client_paiements(client):
    client_paiements = PaiementTry.objects.filter(paiement_by_client__isnull=False, client=client).aggregate(
        amount_status_1=Sum(
            Case(
                When(status=1, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        ),
        amount_status_2=Sum(
            Case(
                When(status=2, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        ),
        amount_status_3=Sum(
            Case(
                When(status=3, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        )
    )
    return client_paiements


def get_direct_sale_paiements(client):
    direct_sale_paiements = PaiementTry.objects.filter(paiement_direct_sale__isnull=False, client=client).aggregate(
        amount_status_1=Sum(
            Case(
                When(status=1, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        ),
        amount_status_2=Sum(
            Case(
                When(status=2, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        ),
        amount_status_3=Sum(
            Case(
                When(status=3, then='amount'),
                default=0,
                output_field=IntegerField( default=0)
            )
        )
    )
    return direct_sale_paiements


def get_all_client_credits(client):
    total_pu_quantity = Commande.objects.filter(client=client).aggregate(
        total=Sum(F('pu') * F('quantity'))
    )
    return total_pu_quantity.get("total", 0)