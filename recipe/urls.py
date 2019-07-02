from django.urls import path, include
from rest_framework import routers
# from .views import RecipeViewSet, RecipeListView, RecipeDetailView, IngredientViewset
from .views import *
from user.views import UserProfileViewset

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewset)
router.register('tags', TagViewset)
router.register('recipes', RecipeViewset)
# This router path is set here because it overrides the other router paths when its in user.urls
router.register('profiles', UserProfileViewset, base_name='profile')


urlpatterns = [
    path('', include(router.urls)),
]
