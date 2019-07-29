from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from user.models import UserAccount, UserProfile
from user.serializers import UserProfileSerializer, UserAccountSerializer, MyTokenObtainPairSerializer


class UserAccountListView(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAdminUser]


class UserAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserSessionView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # print(request.user)
        serializer = UserAccountSerializer(
            request.user, context={'request': request})
        return Response(serializer.data)


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
