# from django_filters import Filter
from django_filters.rest_framework import FilterSet, filters, Filter
from django_filters.widgets import CSVWidget
from .models import *


class RecipeFilterSet(FilterSet):
    tags = filters.CharFilter(
        method='filter_tags'
    )
    title = filters.CharFilter(

    )
    author = filters.CharFilter(
        method='filter_author'
    )

    class Meta:
        model = Recipe
        fields = ['title', 'tags', 'author']

    def filter_tags(self, queryset, tag_text, value):
        return queryset.filter(tags__tag_text__icontains=value)

    def filter_author(self, queryset, username, value):
        return queryset.filter(author__user_account__username=value)
