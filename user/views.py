from rest_framework import viewsets

from user.models import User
from user.serializers import UserProfileSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer