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


class PicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pic
        fields = ['id', 'name', 'position', 'email', 'phone',]
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    function = FunctionSerializer(required=True)
    unit = UnitSerializer(required=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'name',
                  'price', 'quantity',
                  'is_used', 'function', 'unit']
        read_only_fields = ['id', 'is_used', ]
    def _find_and_create_unit(self, unit_data):
        unit, created = Unit.objects.get_or_create(
            name=unit_data.get('name'),
            defaults={
                'abbreviation': unit_data.get('abbreviation'),
                'conversion_rate': unit_data.get('conversion_rate')
            }
        )

        if not created:
            unit.abbreviation = unit_data.get('abbreviation', unit.abbreviation)
            unit.conversion_rate = unit_data.get('conversion_rate', unit.conversion_rate)
            unit.save()

        return unit

    def create(self, validated_data):
        function_data = validated_data.pop('function', {})
        unit_data = validated_data.pop('unit', {})

        function, created = Function.objects.get_or_create(**function_data)
        unit = self._find_and_create_unit(unit_data=unit_data)

        ingredient = Ingredient.objects.create(function=function
                                               , unit=unit, **validated_data)

        return ingredient

    def update(self, instance, validated_data):
        function_data = validated_data.pop('function',{})
        unit_data = validated_data.pop('unit', {})

        function, created = Function.objects.get_or_create(**function_data)
        if not created:
            function.__dict__.update(function_data)
        unit, created = Unit.objects.get_or_create(**unit_data)
        if not created:
            unit.__dict__.update(unit_data)

        ingredient = super().update(instance, validated_data)

        ingredient.function = function
        ingredient.unit = unit

        return ingredient


class SupplierSerializer(serializers.ModelSerializer):
    pic = PicSerializer(required=False, many=True, write_only=True)
    ingredient = IngredientSerializer(required=False, many=True, write_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'location', 'phone', 'pic', 'ingredient']
        read_only_fields = ['id']

    def create(self, validated_data):
        pic_data = validated_data.pop('pic', {})
        ingredient_data = validated_data.pop('ingredient', {})
        supplier, created = Supplier.objects.get_or_create(**validated_data)
        for ingredient in ingredient_data:
            function_data = ingredient.pop('function', {})
            unit_data = ingredient.pop('unit', {})

            function, created = Function.objects.get_or_create(**function_data)
            unit, created = Unit.objects.get_or_create(**unit_data)

            Ingredient.objects.get_or_create(function=function, unit=unit, supplier=supplier, **ingredient)
        for pic in pic_data:
            Pic.objects.get_or_create(supplier=supplier, **pic)
        return supplier

    def update(self, instance, validated_data):
        pic_data = validated_data.pop('pic', [])
        ingredient_data = validated_data.pop('ingredient', [])
        supplier = super().update(instance, validated_data)
        return supplier




