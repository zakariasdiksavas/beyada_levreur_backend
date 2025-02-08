from rest_framework import serializers
from .models import *
from django.conf import settings


class PaiementByCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaiementByCommand
        fields = "__all__"
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        last_paiement_try = PaiementTry.objects.filter(paiement_by_command=data.get("id")).values("paiement_mode", "date", "amount").last()
        if last_paiement_try:
            data.update(last_paiement_try)
        return data
        
        
class PaiementByClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PaiementByClient
        fields = ['id', 'client']
        

class PaimentByDirectSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaimentByDirectSale
        fields = "__all__"
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        last_paiement_try = PaiementTry.objects.filter(paiement_direct_sale=data.get("id")).values("paiement_mode", "date", "amount").last()
        if last_paiement_try:
            data.update(last_paiement_try)
        return data
        
class PaiementProofSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaiementProof
        fields = '__all__'


        
class PaiementTrySerializer(serializers.ModelSerializer):
    proofs = PaiementProofSerializer(many=True, read_only=True)
    class Meta:
        model = PaiementTry
        fields = '__all__'
        