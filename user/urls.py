from django.urls import path, include
from rest_framework import routers
from user.views import UserProfileListView, UserProfileDetailView, UserAccountViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register('account', UserAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('profiles', UserProfileListView.as_view(), name='profile-list'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]