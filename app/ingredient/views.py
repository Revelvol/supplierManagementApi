from rest_framework import generics
from rest_framework import permissions, authentication, status, viewsets
from .serializers import (IngredientSerializer,
                          FunctionSerializer,
                          UnitSerializer,
                          SupplierSerializer,
                          PicSerializer,
                          IngredientDocumentSerializer,
                          SupplierDocumentSerializer,)
from base.models import (Ingredient,
                         Function,
                         Unit,
                         Supplier,
                         Pic,
                         SupplierDocument,
                         IngredientDocument)
from rest_framework.decorators import action
from rest_framework.response import Response
from base.permissions import ReadOnly
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from django.http import Http404

def _params_to_ints(qs):
    """convert list of strings to integers"""
    res = [int(str_id) for str_id in qs.split(",")]
    return res



class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser | ReadOnly]

    def get_queryset(self):
        return self.model.objects.all()

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'function_id',
                OpenApiTypes.STR,
                description='Comma separated list of function IDs to filter ingredient',
            ),
            OpenApiParameter(
                'supplier_id',
                OpenApiTypes.STR,
                description='Comma separated list of supplier IDs to filter ingredient'
            ),
            OpenApiParameter(
                'have_supplier',
                OpenApiTypes.INT, enum=[0, 1],
                description='Int to boolean value to filter ingredient with or without supplier'
            ),
            OpenApiParameter(
                'have_function',
                OpenApiTypes.INT, enum=[0, 1],
                description='Int to boolean value to filter ingredient with or without supplier'
            )
        ]
    )
)
class IngredientViewSet(BaseViewSet):
    """Manage Ingredient Models"""
    model = Ingredient
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        supplier = self.request.query_params.get('supplier_id')
        function = self.request.query_params.get('function_id')
        have_supplier = self.request.query_params.get('have_supplier')
        have_function = self.request.query_params.get('have_function')
        if have_supplier:
            have_supplier = bool(int(have_supplier))
            have_supplier = False if have_supplier else True
            queryset = queryset.filter(supplier__isnull=have_supplier)
        if have_function:
            have_function = bool(int(have_function))
            have_function = False if have_function else True
            queryset = queryset.filter(function__isnull=have_function)

        if supplier:
            supplier_id = _params_to_ints(supplier)
            queryset = queryset.filter(supplier__id__in=supplier_id)
        if function:
            function_id = _params_to_ints(function)
            queryset = queryset.filter(function__id__in=function_id)
        return queryset.order_by('name')


class FunctionViewSet(BaseViewSet):
    """Manage Function Models """
    model = Function
    serializer_class = FunctionSerializer


class UnitViewSet(BaseViewSet):
    """Manage Unit Models"""
    model = Unit
    serializer_class = UnitSerializer


class SupplierViewSet(BaseViewSet):
    """Manage Supplier Models"""
    model = Supplier
    serializer_class = SupplierSerializer

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'supplier_id',
                OpenApiTypes.STR,
                description='Comma separated list of supplier IDs to filter PIC',
            ),
            OpenApiParameter(
                'have_supplier',
                OpenApiTypes.INT, enum=[0, 1],
                description='Int to boolean value to filter pic with or without supplier'
            )
        ]
    )
)

class PicViewSet(BaseViewSet):
    """Manage Pic Models"""
    model = Pic
    serializer_class = PicSerializer
    queryset = Pic.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        supplier = self.request.query_params.get('supplier_id')
        have_supplier = self.request.query_params.get('have_supplier')
        if have_supplier:
            have_supplier = bool(int(have_supplier))
            have_supplier = False if have_supplier else True
            queryset = queryset.filter(supplier__isnull=have_supplier)
        if supplier:
            supplier_id = _params_to_ints(supplier)
            queryset = queryset.filter(supplier__id__in=supplier_id)
        return queryset.order_by('name')


class SupplierDocumentApiView(generics.CreateAPIView ,generics.RetrieveUpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser|ReadOnly]
    lookup_field = 'id'
    serializer_class = SupplierDocumentSerializer

    def post(self, request, id , *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'supplier_id': id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        supplier_id = int(self.kwargs.get(self.lookup_field))
        try:
            queryset = SupplierDocument.objects.get(supplier__id=supplier_id)
            return queryset
        except SupplierDocument.DoesNotExist:
            raise Http404("supplier document not found ")

from django.db.models.query import prefetch_related_objects
class IngredientDocumentApiView(generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    """Upload and Manage one to one relationship of Ingredient Document"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser|ReadOnly]
    serializer_class = IngredientDocumentSerializer
    queryset = IngredientDocument.objects.all()
    lookup_field = 'id'

    def post(self, request, id , *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'ingredient_id': id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        ingredient_id = int(self.kwargs.get(self.lookup_field))
        queryset = IngredientDocument.objects.get(ingredient__id=ingredient_id)
        return queryset











