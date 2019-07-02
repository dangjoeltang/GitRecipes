from django.urls import path, include
from rest_framework import routers
# from .views import RecipeViewSet, RecipeListView, RecipeDetailView, IngredientViewset
from .views import *
from user.views import UserProfileViewset

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewset)
router.register('tags', TagViewset)
router.register('recipes', RecipeViewset)
router.register('profiles', UserProfileViewset, base_name='profile')


urlpatterns = [
    path('', include(router.urls)),
]
