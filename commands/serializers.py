from rest_framework import serializers
from .models import *



class CommandeSerializer(serializers.ModelSerializer):
    batiment_name = serializers.CharField(source='batiment.name', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    site_name = serializers.CharField(source='batiment.site.name', read_only=True)
    site_id = serializers.CharField(source='batiment.site.id', read_only=True)
    class Meta:
        model = Commande
        fields = [
            'id', 'batiment', 'batiment_name', 'client_name', 'site_id', 'site_name', 'client', 'created_by', 
            'quantity', 'poids_plateau', 'pu', 'description', 'classe',
            'is_delivered', 'auto_created', 'date', 'production_source'
        ]