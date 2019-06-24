from django.urls import path, include
from rest_framework import routers
# from .views import RecipeViewSet, RecipeListView, RecipeDetailView, IngredientViewset
from .views import *

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewset)
router.register('tags', TagViewset)
router.register('test', RecipeViewset)

urlpatterns = [
    path('', include(router.urls)),
    # path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/<pk>/ingredients/', RecipeIngredientListView.as_view(),
         name='recipe-ingredients-list'),
    path('recipes/<pk>/ingredients/<id>/',
         RecipeIngredientDetailView.as_view(), name='recipe-ingredients-detail'),
    path('recipes/<pk>/tags/', RecipeTagListView.as_view(), name='recipe-tags-list'),
    path('recipes/<pk>/tags/<id>/', RecipeTagDetailView.as_view(),
         name='recipe-tags-detail'),
    path('recipes/<pk>/steps/', RecipeStepListView.as_view(),
         name='recipe-steps-list'),
    path('recipes/<pk>/steps/<step_number>/',
         RecipeStepDetailView.as_view(), name='recipe-steps-detail'),
    path('recipes/<pk>/notes/', RecipeNoteListView.as_view(),
         name='recipe-notes-list'),
    path('recipes/<pk>/notes/<id>/', RecipeNoteDetailView.as_view(),
         name='recipe-notes-detail'),

]
