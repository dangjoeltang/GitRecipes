from .serializers import *
from .models import *
import json
import requests
import sys
import os
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import RecipeFilterSet

from recipe.permissions import *

from django.http import JsonResponse
import boto3
from botocore.config import Config


class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class TagViewset(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = GenericRecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]

    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilterSet
    # filter_fields = ('tags',)

    # def get_queryset(self):
    #     queryset = Recipe.objects.all()
    #     profile = self.request.query_params.get('profile', None)
    #     if profile is not None:
    #         queryset = queryset.filter(author=profile)
    #     return queryset


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sign_s3(request):
    S3_BUCKET = 'gitrecipes-media'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    region = 'us-east-2'
    file_name = request.data.get('file_name')
    file_type = request.data.get('file_type')

    s3 = boto3.client(
        's3',
        region_name=region,
        # config=Config(signature_version='s3v4'),
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    presigned_post = s3.generate_presigned_post(
        Bucket=S3_BUCKET,
        Key=file_name,
        Fields={
            # 'acl': 'public-read',
            "Content-Type": file_type
        },
        Conditions=[
            # {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn=100  # seconds
    )

    return JsonResponse({
        'data': presigned_post,
        'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name),
        'path': file_name
    })
