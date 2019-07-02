from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins

from .models import *
from .serializers import *


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientDetailSerializer


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = GenericRecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        profile = self.request.query_params.get('profile', None)
        if profile is not None:
            queryset = queryset.filter(author=profile)
        return queryset
