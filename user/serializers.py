from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import UserAccount, UserProfile
from recipe.models import Recipe


class UserProfileSerializer(serializers.ModelSerializer):
    author_recipes = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='recipe-detail',
    )

    recipe_count = serializers.IntegerField(
        source='author_recipes.count', read_only=True)
    profile_photo = serializers.CharField(
        allow_blank=True, required=False
    )

    class Meta:
        model = UserProfile
        fields = ('id', 'user_account', 'username', 'first_name',
                  'last_name', 'short_bio', 'profile_photo', 'recipe_count', 'author_recipes', 'created_time')
        extra_kwargs = {
            'url': {'view_name': 'profile-detail'},
        }
        lookup_field = 'username'


class UserAccountSerializer(serializers.ModelSerializer):
    # profile = serializers.HyperlinkedRelatedField(
    #     required=False,
    #     view_name='profile-detail',
    #     # queryset=UserProfile.objects.all(),
    #     read_only=True,
    #     lookup_field='profile'
    # )

    class Meta:
        model = UserAccount
        fields = ('id', 'profile', 'email', 'username', 'password',
                  'first_name', 'last_name')
        # fields = '__all__'
        extra_kwargs = {
            # 'url': {'view_name': 'account-detail'},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserAccount(**validated_data)
        user.set_password(password)
        user.save()
        profile = UserProfile.objects.create(
            user_account=user,
            # username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['profile_id'] = user.profile.id
        # token['email'] = user.email
        # ...

        return token
