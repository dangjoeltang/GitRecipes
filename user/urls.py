from django.urls import path, include
from rest_framework import routers
from user.views import UserSessionView, UserProfileViewset, UserAccountListView, UserAccountDetailView, MyTokenObtainPairView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # These paths are all admin paths only
    path('accounts/', UserAccountListView.as_view(), name='account-list'),
    path('accounts/<int:pk>', UserAccountDetailView.as_view(), name='account-detail'),

    # This path is used to check user session
    path('user/', UserSessionView.as_view(), name='user-session'),

    # These paths are public
    # path('profiles/', UserProfileView.as_view(), name='profile-list'),
    # path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # path('login/', api_login, name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
