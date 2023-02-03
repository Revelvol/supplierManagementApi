from rest_framework.views import APIView
from rest_framework import permissions, authentication
from .serializers import (IngredientSerializer)
from base.models import Ingredient
from rest_framework import status, generics , viewsets
from base.permissions import ReadOnly



class IngredientViewSet(viewsets.ModelViewSet):
    """manage ingredient models"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser|ReadOnly]# add staff can write

    def get_queryset(self):
        return Ingredient.objects.all()




