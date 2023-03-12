from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response

from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer


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

        if user.check_password(current_password):
            if current_password != new_password:
                user.password = make_password(new_password)
                user.save()

                response = {'detail': 'password changed successfully'}
                return Response(response)

            response = {'detail': 'enter different password from your current one!'}
            return Response(response)

        response = {'detail': 'password is not correct'}
        return Response(response)
