from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from base.models import (Ingredient,
                         Function,
                         Unit,
                         Supplier,
                         Pic, )


class FunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ['id', 'name']
        read_only_fields = ['id']


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name',
                  'abbreviation', 'conversion_rate', ]
        read_only_fields = ['id']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'location', 'phone']
        read_only_fields = ['id']


class PicSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(required=True)

    class Meta:
        model = Pic
        fields = ['id', 'name', 'position', 'email', 'phone', 'supplier']
        read_only_fields = ['id']

    def create(self, validated_data):
        supplier_data = validated_data.pop('supplier')
        supplier, created = Supplier.objects.get_or_create(**supplier_data)
        pic = Pic.objects.create(supplier=supplier, **validated_data)
        return pic

    def update(self, instance, validated_data):
        supplier_data = validated_data.pop('supplier')
        supplier, created = Supplier.objects.get_or_create(**supplier_data)
        pic = super().update(instance, validated_data)
        pic.supplier = supplier
        return pic


class IngredientSerializer(serializers.ModelSerializer):
    function = FunctionSerializer(required=True)
    unit = UnitSerializer(required=True)
    supplier = SupplierSerializer(required=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name',
                  'price', 'quantity',
                  'is_used', 'function',
                  'supplier', 'unit']
        read_only_fields = ['id', 'is_used', ]

    def create(self, validated_data):
        function_data = validated_data.pop('function')
        supplier_data = validated_data.pop('supplier')
        unit_data = validated_data.pop('unit')

        supplier, created = Supplier.objects.get_or_create(**supplier_data)
        function, created = Function.objects.get_or_create(**function_data)
        unit, created = Unit.objects.get_or_create(**unit_data)

        ingredient = Ingredient.objects.create(supplier=supplier, function=function
                                               , unit=unit, **validated_data)

        return ingredient

    def update(self, instance, validated_data):
        function_data = validated_data.pop('function')
        supplier_data = validated_data.pop('supplier')
        unit_data = validated_data.pop('unit')

        supplier, created = Supplier.objects.get_or_create(**supplier_data)
        function, created = Function.objects.get_or_create(**function_data)
        unit, created = Unit.objects.get_or_create(**unit_data)

        ingredient = super().update(instance, validated_data)

        ingredient.supplier = supplier
        ingredient.function = function
        ingredient.unit = unit

        return ingredient
