from django.urls import path, include
from rest_framework import routers
# from .views import RecipeViewSet, RecipeListView, RecipeDetailView, IngredientViewset
from .views import *

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewset)
router.register('tags', TagViewset)
router.register('recipes', RecipeViewset)

urlpatterns = [
    path('', include(router.urls)),
]
