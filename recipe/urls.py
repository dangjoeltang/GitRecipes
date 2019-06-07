from django.urls import path, include
from rest_framework import routers
# from .views import RecipeViewSet, RecipeListView, RecipeDetailView, IngredientViewset
from .views import *

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewset)
router.register('tags', TagViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail')
]
