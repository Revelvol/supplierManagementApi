from rest_framework import routers
from .views import (IngredientViewSet,
                    FunctionViewSet,
                    UnitViewSet,
                    SupplierViewSet,
                    PicViewSet,
                    SupplierDocumentApiView,)
from django.urls import path

router = routers.SimpleRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'functions', FunctionViewSet, basename='function')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r"pic's", PicViewSet, basename='pic')

app_name = 'ingredient'

urlpatterns = [
    path('suppliers/<int:id>/upload-document/', SupplierDocumentApiView.as_view(), name = "supplier-document-upload")
    ]

urlpatterns += router.urls
