from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


def matchmaking():
    pass


def join_match():
    pass


def reduce_coin():
    pass


class StartMatchView(APIView):
    pass


class MatchViewSet(mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    pass


class QuitMatchView(APIView):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class GenerateRandomCategoryView(APIView):
    pass


class QuestionViewSet(viewsets.ModelViewSet):
    pass


class GenerateRandomQuestionView(APIView):
    pass


class ChoicesViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    pass


class AnswerQuestionView(APIView):
    pass


class FinishMatch(APIView):
    pass


class PlayerAnswerViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    pass


def remove_incorrect_choices_help():
    pass


def popular_choices_help():
    pass


def second_chance_help():
    pass
