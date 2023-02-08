from rest_framework.views import APIView
from rest_framework import permissions, authentication
from .serializers import (IngredientSerializer,
                          FunctionSerializer,
                          UnitSerializer,
                          SupplierSerializer,
                          PicSerializer,)
from base.models import (Ingredient,
                         Function,
                         Unit,
                         Supplier,
                         Pic,)
from rest_framework import status, generics, viewsets
from base.permissions import ReadOnly


class BaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser | ReadOnly]

    def get_queryset(self):
        return self.model.objects.all()


class IngredientViewSet(BaseViewSet):
    """Manage Ingredient Models"""
    model = Ingredient
    serializer_class = IngredientSerializer


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


class PicViewSet(BaseViewSet):
    """Manage Pic Models"""
    model = Pic
    serializer_class = PicSerializer






