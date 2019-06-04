from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import UserAccount, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    # user_account = serializers.HyperlinkedRelatedField(view_name='useraccount-detail', read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user_account', 'first_name', 'last_name')


class UserAccountSerializer(serializers.HyperlinkedModelSerializer):

    profile = UserProfileSerializer(
        required=True,
    )


    class Meta:
        model = UserAccount
        # fields = ('pk', 'username', 'email', 'password', 'profile')
        fields = ('id', 'url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {
            'url': {'view_name': 'userprofile-detail'},
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