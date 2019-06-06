from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import UserAccount, UserProfile
from recipe.models import Recipe


class UserProfileSerializer(serializers.ModelSerializer):
    # author_recipes = serializers.HyperlinkedIdentityField(
    #     view_name='recipe-list',
    #     many=True,
    # )

    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'userprofile-detail'},
        }


class UserAccountSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(
        read_only=True,
        required=False
    )


    class Meta:
        model = UserAccount
        fields = ('id', 'url', 'email', 'username', 'first_name', 'last_name', 'profile')
        extra_kwargs = {
            'url': {'view_name': 'useraccount-detail'},
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