from rest_framework import viewsets

from .models import *
from .serializers import *


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer