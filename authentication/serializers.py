from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserExt
from base.models import Site

class UserExtSerializer(serializers.ModelSerializer):
    sites = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Site.objects.all()
    )
    class Meta:
        model = UserExt
        fields = ['user', 'sites', 'phone', 'eleveur']
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}