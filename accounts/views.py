from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Player
from .serializers import UserRegisterSerializer, UserSerializer, UserInfoSerializer, ChangePasswordSerializer, \
    UserFullSerializer, ProfileSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()


class UserView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise AuthenticationFailed('unauthenticated')


class UserInfoView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise AuthenticationFailed('unauthenticated')


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserFullSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise AuthenticationFailed('unauthenticated')


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        raise AuthenticationFailed('unauthenticated')

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        current_password = request.data['current_password']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']

        if user.check_password(current_password):
            validate_password(new_password)

            if current_password != new_password:
                if new_password == confirm_password:
                    user.password = make_password(new_password)
                    user.save()

                    response = {'detail': 'password changed successfully'}
                    return Response(response)

                response = {'detail': 'password and  confirm password do not match'}
                return Response(response)

            response = {'detail': 'enter different password from your current one!'}
            return Response(response)

        response = {'detail': 'password is not correct'}
        return Response(response)


class ProfileView(APIView):
    def get(self, request):
        user = request.user
        if not user:
            raise AuthenticationFailed('unauthenticated')

        profile = Player.objects.filter(user_id=user.id).first()

        if not profile:
            response = {'detail': 'profile not found!'}
            return Response(response)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
