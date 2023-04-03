from rest_framework import serializers
from base.models import (Ingredient,
                         Function,
                         Unit,
                         Supplier,
                         Pic,
                         SupplierDocument,
                         IngredientDocument)


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
        fields = ['id', 'name', 'position', 'email', 'phone']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    function = FunctionSerializer(required=True)
    unit = UnitSerializer(required=True)

    class Meta:
        model = Ingredient
        fields = ['id', 'supplier', 'name',
                  'price', 'quantity',
                  'is_used', 'function', 'unit']
        read_only_fields = ['id', ]

    def _find_and_create_unit(self, unit_data): # still have bug where the returned value is still updated
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

        function , created = Function.objects.get_or_create(**function_data)
        unit = self._find_and_create_unit(unit_data=unit_data)

        ingredient = Ingredient.objects.create(function=function
                                               , unit=unit, **validated_data)

        return ingredient

    def update(self, instance, validated_data):
        function_data = validated_data.pop('function',{})
        unit_data = validated_data.pop('unit', {})

        function, created = Function.objects.get_or_create(**function_data)
        unit = self._find_and_create_unit(unit_data=unit_data)
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
        validated_data.pop('pic', [])
        validated_data.pop('ingredient', [])
        supplier = super().update(instance, validated_data)
        return supplier


class IngredientDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientDocument
        fields = ['ingredient', 'isoDocument', 'gmoDocument', 'kosherDocument',
                  'halalDocument','msdsDocument', 'tdsDocument','coaDocument','allergenDocument',]
        read_only_fields = ['ingredient']

    def create(self, validated_data):
        ingredient_document = IngredientDocument.objects.create(
            ingredient=Ingredient.objects.get(id=int(self.context["ingredient_id"])),
            **validated_data)

        return ingredient_document


class SupplierDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierDocument
        fields = ['supplier', 'isoDocument', 'gmpDocument', 'haccpDocument']
        read_only_fields = [ 'supplier']

    def create(self, validated_data):
        supplier_document = SupplierDocument.objects.create(supplier=Supplier.objects.get(id=int(self.context["supplier_id"])),
                                                            **validated_data)

        return supplier_document