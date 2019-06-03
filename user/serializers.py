from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    profile = UserProfileSerializer(
        required=True,
    )


    class Meta:
        model = User
        # fields = ('pk', 'username', 'email', 'password', 'profile')
        fields = ('pk', 'url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {
            'url': {'view_name': 'profile-detail'},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
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