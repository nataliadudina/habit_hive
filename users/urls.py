from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserApiList, UserRegistrationAPIView, UserUpdateApiList, UserDestroyApiView, UserDetailApiList

app_name = UsersConfig.name

urlpatterns = [
    path('users/', UserApiList.as_view(), name='user-get'),
    path('register/', UserRegistrationAPIView.as_view(), name='user-post'),
    path('users/<int:pk>/', UserDetailApiList.as_view(), name='profile'),
    path('users/<int:pk>/edit/', UserUpdateApiList.as_view(), name='profile-put-patch'),
    path('users/<int:pk>/delete/', UserDestroyApiView.as_view(), name='user-destroy'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
