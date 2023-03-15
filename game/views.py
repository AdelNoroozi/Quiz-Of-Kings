import random

from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
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

    @action(detail=True, methods=['PATCH'])
    def add_selected_category(self, request, pk=None):
        match = Match.objects.get(id=pk)
        category_id = request.data['category_id']
        category = Category.objects.get(id=category_id)
        match.selected_categories.add(category)
        match.save()
        response = {'message': 'category added successfully'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH'])
    def finish_round(self, request, pk=None):
        match = Match.objects.get(id=pk)
        if match.rounds_played >= 6:
            response = {'message': 'this match has already reached to its maximum possible rounds'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            match.rounds_played += 1
            match.save()
            response = {'message': 'round finished successfully'}
            return Response(response, status=status.HTTP_200_OK)


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

    @action(detail=True, methods=['GET'])
    def remove_incorrect_choices_help(self, request, pk=None):
        question = Question.objects.get(id=pk)
        retrieving_choices = Choice.objects.filter(question=question, is_correct=False).order_by('?')[0:2]
        reduce_coin(10)
        serializer = ChoiceMiniSerializer(retrieving_choices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    def post(self, request):
        # user = request.user
        try:
            # user is temporarily gathered by id
            user_id = request.data['user_id']
            match_id = request.data['match_id']
            question_id = request.data['question_id']
            answer_id = request.data['answer_id']
        except:
            response = {'message': 'invalid fields'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                match = Match.objects.get(id=match_id)
                question = Question.objects.get(id=question_id)
                choice = Choice.objects.get(id=answer_id)
                player = Player.objects.get(user_id=user_id)
            except:
                response = {'message': 'could not find objects with specified ids'}
                return Response(response, status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    PlayerAnswer.objects.get(player=player, match=match, question=question)
                except:
                    if match.starter_player == player:
                        if match.turn == 'J':
                            response = {'message': 'it is not this players turn'}
                            return Response(response, status=status.HTTP_403_FORBIDDEN)
                    elif match.joining_player == player:
                        if match.turn == 'S':
                            response = {'message': 'it is not this players turn'}
                            return Response(response, status=status.HTTP_403_FORBIDDEN)
                    question.answered_count += 1
                    question.save()
                    choice.chosen_count += 1
                    choice.save()
                    if choice.is_correct:
                        if match.starter_player == player:
                            match.starter_player_score += 1
                            match.save()
                        elif match.joining_player == player:
                            match.joining_player_score += 1
                            match.save()
                    player_answer = PlayerAnswer.objects.create(match=match, player=player, question=question,
                                                                answer=choice)
                    serializer = PlayerAnswerSerializer(player_answer)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    response = {'message': 'player has already answered this question in this match'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Sajjad
class FinishMatch(APIView):
    pass


# Sajjad
class PlayerAnswerViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    pass


# Sajjad
def popular_choices_help():
    pass

# def second_chance_help():
#     pass
