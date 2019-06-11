from rest_framework import viewsets
from rest_framework import generics

from .models import *
from .serializers import *


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object 
        self.check_object_permissions(self.request, obj)
        return obj


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
        # print(RecipeIngredient.objects.filter(recipe__pk = recipe_pk))
        return RecipeIngredient.objects.filter(recipe__pk = recipe_pk)


class RecipeIngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSetSerializer
    lookup_field = 'id'

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        recipe_ingredient_pk = self.kwargs['id']

        return RecipeIngredient.objects.filter(recipe__pk = recipe_pk)