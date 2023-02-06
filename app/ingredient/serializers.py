from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from base.models import (Ingredient,
                         Function,
                         Unit,
                         Supplier,
                         Pic,)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name',
                  'price', 'quantity',
                  'is_used', ]
        read_only_fields = ['id', 'is_used', ]


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ['id', 'name']
        read_only_fields = ['id']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name',
                  'abbreviation', 'conversion_rate',]
        read_only_fields = ['id']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'location', 'phone']
        read_only_fields = ['id']

class PicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = ['id', 'name', 'position', 'email', 'phone']
        read_only_fields = ['id']

