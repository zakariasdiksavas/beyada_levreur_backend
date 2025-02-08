from rest_framework import serializers
from .models import *



class DirectSaleSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    batiment_name = serializers.CharField(source='batiment.name', read_only=True)
    site_name = serializers.CharField(source='batiment.site.name', read_only=True)
    site_id = serializers.CharField(source='batiment.site.id', read_only=True)
    client_id = serializers.CharField(source='client.id', read_only=True)
    batiment_id = serializers.CharField(source='batiment.id', read_only=True)


    class Meta:
        model = DirectSale
        fields = ["id", "batiment", "client", "site_id", "client_id", "batiment_id", "client_name", "batiment_name", "site_name", "init_pu", "day_pu", "quantity", "change", "date", "classe"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add additional fields that are not part of the model but are required in the response
        representation['client__name'] = instance.client.name
        representation['batiment__name'] = instance.batiment.name
        representation['batiment__site__name'] = instance.batiment.site.name
        return representation
        
        