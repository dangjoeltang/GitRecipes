from django.urls import path, include
from rest_framework import routers
from user.views import UserProfileListView, UserProfileDetailView, UserAccountListView, UserAccountDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('accounts/', UserAccountListView.as_view(), name='account-list'),
    path('accounts/<int:pk>', UserAccountDetailView.as_view(), name='account-detail'),
    path('profiles/', UserProfileListView.as_view(), name='profile-list'),
    path('profiles/<user_account__username>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]