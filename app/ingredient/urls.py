from rest_framework import routers
from .views import (IngredientViewSet,
                    FunctionViewSet,
                    UnitViewSet,
                    SupplierViewSet,
                    PicViewSet,)

router = routers.SimpleRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'functions', FunctionViewSet, basename='function')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'suppliers', SupplierViewSet, basename='supplier')
router.register(r"pic's", PicViewSet, basename='pic')

app_name = 'ingredient'

urlpatterns = [
    ]

urlpatterns += router.urls
