from django.urls import path, include
from rest_framework import routers
from user.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register('profile', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]