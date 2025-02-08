from rest_framework import serializers
from .models import Inventaire

class InventaireSerializer(serializers.ModelSerializer):
    batiment_name = serializers.CharField(source='batiment.name', read_only=True)
    site_name = serializers.CharField(source="batiment.site.name", read_only=True)
    site_id = serializers.CharField(source="batiment.site.id", read_only=True)
    class Meta:
        model = Inventaire
        fields = '__all__'