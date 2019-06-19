from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import UserAccount, UserProfile
from user.serializers import UserProfileSerializer, UserAccountSerializer, MyTokenObtainPairSerializer


class UserAccountListView(generics.ListCreateAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class UserAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer


class UserSessionView(generics.RetrieveAPIView):
    def get(self, request):
        print(request.user)
        serializer = UserAccountSerializer(request.user, context={'request': request})
        return Response(serializer.data)


class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # lookup_fields = ('user_account__username', 'id')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# @api_view(['POST'])
# def api_login(request):
#     data = JsonReader.read_body(request)

