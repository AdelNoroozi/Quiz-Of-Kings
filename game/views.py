from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .models import Question, Choice, PlayerAnswer
from .serializers import ChoiceSerializer, PlayerAnswerSerializer


# later
def matchmaking():
    pass


# later
def join_match():
    pass


# sajjad
def reduce_coin(player, coins):
    if player.coin >= coins:
        player.coin -= coins
    else:
        player.coin = 0

    player.save()


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
class ChoicesViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()


# Adel
class AnswerQuestionView(APIView):
    pass


# Sajjad
class FinishMatch(APIView):
    pass


# Sajjad
class PlayerAnswerViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = PlayerAnswerSerializer
    queryset = PlayerAnswer.objects.all()


# Adel
def remove_incorrect_choices_help():
    pass


# Sajjad
def popular_choices_help(question_id):
    choices = Choice.objects.filter(question_id=question_id).values('pk', 'chosen_count')
    return choices

# def second_chance_help():
#     pass
