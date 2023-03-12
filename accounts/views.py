from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import UserRegisterSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

