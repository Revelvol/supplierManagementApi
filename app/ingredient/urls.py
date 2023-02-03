from rest_framework import routers
from .views import (IngredientViewSet)

router = routers.SimpleRouter()
router.register(r'ingredients', IngredientViewSet)

app_name = 'ingredient'

urlpatterns = [
    ]

urlpatterns += router.urls