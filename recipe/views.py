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


class RecipeListView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeTagListView(generics.ListCreateAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeTag.objects.filter(recipe__pk = recipe_pk)


class RecipeTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeTag.objects.all()
    serializer_class = RecipeTagSerializer
    lookup_field = 'id'

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeTag.objects.filter(recipe__pk = recipe_pk)


class RecipeIngredientListView(generics.ListCreateAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSetSerializer

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeIngredient.objects.filter(recipe__pk = recipe_pk)


class RecipeIngredientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSetSerializer
    lookup_field = 'id'

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        recipe_ingredient_pk = self.kwargs['id']

        return RecipeIngredient.objects.filter(recipe__pk = recipe_pk)


class RecipeStepListView(generics.ListCreateAPIView):
    queryset = RecipeStep.objects.all()
    serializer_class = RecipeStepSerializer

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeStep.objects.filter(recipe__pk = recipe_pk)


class RecipeStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeStep.objects.all()
    serializer_class = RecipeStepSerializer
    lookup_field = 'step_number'

    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeStep.objects.filter(recipe__pk = recipe_pk)


class RecipeNoteListView(generics.ListCreateAPIView):
    queryset = RecipeNote.objects.all()
    serializer_class = RecipeNoteSerializer
    
    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeNote.objects.filter(recipe__pk = recipe_pk)


class RecipeNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RecipeNote.objects.all()
    serializer_class = RecipeNoteSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        recipe_pk = self.kwargs['pk']
        return RecipeNote.objects.filter(recipe__pk = recipe_pk)