from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import UserAccount, UserProfile
from recipe.models import Recipe
from recipe.serializers import RecipeListSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    author_recipes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recipe-detail'
    )

    user_account = serializers.StringRelatedField()
    recipe_count = serializers.IntegerField(source='author_recipes.count', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('id', 'user_account', 'first_name', 'last_name', 'recipe_count', 'author_recipes')
        extra_kwargs = {
            'url': {'view_name': 'profile-detail'},
        }


class UserAccountSerializer(serializers.ModelSerializer):
    profile = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='profile-detail'
    )

    class Meta:
        model = UserAccount
        fields = ('id', 'url', 'email', 'username', 'first_name', 'last_name', 'profile')
        extra_kwargs = {
            'url': {'view_name': 'account-detail'},
            'password': {'write_only': True}
        }

        

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = UserAccount(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user_account=user, **profile_data)
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.first_name = profile_data.get('first_name', profile.first_name)
        profile.last_name = profile_data.get('last_name', profile.last_name)
        profile.save()

        return instance