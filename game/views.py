from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


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
    pass


# Adel
class QuitMatchView(APIView):
    pass


# Adel
class CategoryViewSet(viewsets.ModelViewSet):
    pass


# Adel
class GenerateRandomCategoryView(APIView):
    pass


# Adel
class QuestionViewSet(viewsets.ModelViewSet):
    pass


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
