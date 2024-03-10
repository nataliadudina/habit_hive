from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habit.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, UserProfileSerializer


class UserApiList(generics.ListAPIView):
    """ View for listing users """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated]


class UserRegistrationAPIView(generics.CreateAPIView):
    """ View for user registration """
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
    """ View for retrieving user details """
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Successful response description", UserSerializer),
            404: 'Not found'
        },
        operation_description="Get user profile",
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_serializer_class(self):
        """ Get the serializer class based on the user """
        user = self.get_object()

        if user == self.request.user:
            return UserProfileSerializer  # View own profile
        else:
            return UserSerializer  # View other profiles


class UserUpdateApiList(generics.UpdateAPIView):
    """ Update user information """
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
    """ View for deleting a user """
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
