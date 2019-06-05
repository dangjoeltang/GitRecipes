from django.urls import path, include
from rest_framework import routers
from .views import RecipeViewSet, RecipeListView, RecipeDetailView

# router = routers.DefaultRouter()
# router.register('recipes', RecipeList())
# # router.register('recipes', RecipeList.as_view(), name='recipe-list')

urlpatterns = [
    # path('', include(router.urls)),
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail')
]
