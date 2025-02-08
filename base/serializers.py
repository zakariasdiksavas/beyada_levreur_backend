from rest_framework import serializers
from .models import *



class EleveurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleveur
        fields = ['id', 'name', 'address', 'phone', 'email']


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'name', 'address', 'eleveur']


class BatimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batiment
        fields = ['id', 'name', 'site']
        
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'eleveur', 'name', 'address', 'phone', 'email']
        
        
class ClientBatimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBatiment
        fields = ['id', 'client', 'batiment', 'is_linked']