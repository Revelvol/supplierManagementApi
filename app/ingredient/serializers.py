from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from base.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name',
                  'price', 'quantity',
                  'is_used', ]
        read_only_fields = ['id', 'is_used', ]