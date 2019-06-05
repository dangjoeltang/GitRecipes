from django.urls import path, include
from rest_framework import routers
from user.views import UserProfileViewSet, UserAccountViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register('profile', UserProfileViewSet)
router.register('account', UserAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]