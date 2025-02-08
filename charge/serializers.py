from rest_framework import serializers
from .models import *


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ['id', 'commande', 'driver', 'datetime', 'change', "eggs_produced_at", "quantity", "classe"]