from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habit.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, UserProfileSerializer


class UserApiList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()


class UserDetailApiList(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        user = self.get_object()

        if user == self.request.user:
            return UserProfileSerializer    # просмотр собственного профиля
        else:
            return UserSerializer    # просмотр чужого профиля


class UserUpdateApiList(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()


class UserDestroyApiView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
