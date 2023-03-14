import random

from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers
from game.models import *
from game.serializers import *


# later
def matchmaking():
    pass


# later
def join_match():
    pass


# sajjad
def reduce_coin(coins):
    pass


# later
class StartMatchView(APIView):
    pass


# Adel
class MatchViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()


# Adel
class QuitMatchView(APIView):
    pass


# Adel
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# Adel
class GenerateRandomCategoryView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_active=True).order_by('?')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Adel
class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


# Sajjad
class GenerateRandomQuestionView(APIView):
    pass


# Sajjad
class ChoicesViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    pass


# Adel
class AnswerQuestionView(APIView):
    pass


# Sajjad
class FinishMatch(APIView):
    pass


# Sajjad
class PlayerAnswerViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    pass


# Adel
def remove_incorrect_choices_help():
    pass


# Sajjad
def popular_choices_help():
    pass

# def second_chance_help():
#     pass
