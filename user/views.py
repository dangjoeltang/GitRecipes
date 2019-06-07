from rest_framework import viewsets
from rest_framework import generics


from user.models import UserAccount, UserProfile
from user.serializers import UserProfileSerializer, UserAccountSerializer


class UserAccountListView(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class UserAccountDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # lookup_fields = ('user_account__username', 'id')