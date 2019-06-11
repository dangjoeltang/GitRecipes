from django.urls import path, include
from rest_framework import routers
# from .views import RecipeViewSet, RecipeListView, RecipeDetailView, IngredientViewset
from .views import *

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewset)
router.register('tags', TagViewset)
# router.register('recipes/<int:pk>/ingredients/', RecipeIngredientSetView)

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/<int:pk>/ingredients/', RecipeIngredientSetView.as_view(), name='recipe-ingredients-list'),
    path('recipes/<int:pk>/ingredients/<int:id>/', RecipeIngredientDetailView.as_view(), name='recipe-ingredients-detail')

]
