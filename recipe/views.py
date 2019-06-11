from rest_framework import viewsets
from rest_framework import generics

from .models import *
from .serializers import *


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeListView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeIngredientSetView(generics.ListCreateAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSetSerializer

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeIngredient.objects.filter(recipe__pk = recipe_pk)


class RecipeIngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSetSerializer
    lookup_fields = ('id')

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        recipe_ingredient_pk = self.kwargs['id']

        return RecipeIngredient.objects.get(id=recipe_ingredient_pk)