import random

from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers

from accounts.models import User
from game.models import *
from game.serializers import *


# later
def matchmaking(user):
    player = Player.objects.filter(user_id=user.id).first()
    if not player:
        response = {'detail': 'player Not found!'}
        return Response(response)
    try:
        match = Match.objects.create(starter_player=player, status='MM')
    except Exception as e:
        response = {'detail': str(e)}
        return Response(response)

    return match


# later
def join_match(match: Match, user: User):
    player = Player.objects.filter(user_id=user.id).first()
    if not player:
        response = {'message': 'player not found'}
        return Response(response, status=status.HTTP_404_NOT_FOUND)
    match.joining_player = player
    match.status = 'OG'
    match.save()
    return match


# sajjad
def reduce_coin(player, coins):
    if player.coin >= coins:
        player.coin -= coins
    else:
        player.coin = 0

    player.save()


# later
class StartMatchView(APIView):
    def post(self, request):
        ready_matches = Match.objects.filter(status='MM')
        user = request.user

        if user.is_anonymous:
            raise AuthenticationFailed('unauthenticated')

        if not ready_matches:
            match = matchmaking(user)
            serializer = MatchMiniSerializer(match)
            return Response(serializer.data)

        else:
            player = Player.objects.filter(user_id=user.id).first()
            match = ready_matches.order_by('?').first()

            if match.starter_player.id == player.id:
                match = matchmaking(user)
                serializer = MatchMiniSerializer(match)
                return Response(serializer.data)

            match = join_match(user=user, match=match)
            serializer = MatchMiniSerializer(match)
            return Response(serializer.data)


# Adel
class MatchViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    @action(detail=True, methods=['PATCH'])
    def add_selected_category(self, request, pk=None):
        match = Match.objects.get(id=pk)
        if not match:
            response = {'message': 'match NOT found!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            category_id = request.data['category_id']
        except Exception as e:
            response = {'message': str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.get(id=category_id)
        if not match:
            response = {'message': 'category NOT found!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        match.selected_categories.add(category)
        match.save()
        response = {'message': 'category added successfully'}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH'])
    def finish_round(self, request, pk=None):
        match = Match.objects.get(id=pk)
        if not match:
            response = {'message': 'match NOT found!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if match.rounds_played >= 6:
            response = {'message': 'this match has already reached to its maximum possible rounds'}
            return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            match.rounds_played += 1
            match.save()
            response = {'message': 'round finished successfully'}
            return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH'])
    def change_turn(self, request, pk=None):
        match = Match.objects.get(id=pk)
        if not match:
            response = {'message': 'match NOT found!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        turn = ''
        if match.turn == 'S':
            match.turn = 'J'
            match.save()
            turn = 'joining player'

        elif match.turn == 'J':
            match.turn = 'S'
            match.save()
            turn = 'starter player'

        response = {'message': f'turn changed to {turn} successfully'}
        return Response(response, status=status.HTTP_200_OK)


# Adel
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(detail=True, methods=['GET'])
    def random_questions(self, request, pk=None):
        questions = Question.objects.filter(category_id=pk).order_by('?')[:3]
        if questions is None:
            response = {'detail': 'there are no questions in this category'}
            return Response(response)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


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
        reduce_coin(10)  # todo get player and pass it to function
        serializer = ChoiceMiniSerializer(retrieving_choices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Sajjad
class ChoicesViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()


# Adel
class AnswerQuestionView(APIView):
    def post(self, request):
        user = request.user
        if user.is_anonymous:
            raise AuthenticationFailed('unauthenticated')
        try:
            match_id = request.data['match_id']
            question_id = request.data['question_id']
            answer_id = request.data['answer_id']
        except Exception as e:
            response = {'message': str(e)}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                match = Match.objects.get(id=match_id)
                question = Question.objects.get(id=question_id)
                choice = Choice.objects.get(id=answer_id)
                player = Player.objects.get(user_id=user.id)
            except Exception as e:
                response = {'message': str(e)}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
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
def finish_match(match_id, state):
    match = Match.objects.filter(id=match_id).first()
    if not match:
        response = {'message': 'match NOT found!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    elif match.status == 'finished':
        response = {'message': 'match NOT found (already finished)!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    elif match.status == 'quited':
        response = {'message': 'match NOT found (already quited)!'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    elif match.status == 'ongoing':
        if state == 'finished' or state == 'quited':
            match.status = state
            match.save()

            response = {'message': f'match state changed to {state}!'}
            return Response(response, status=status.HTTP_200_OK)

        response = {'message': 'status is not valid'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


# Sajjad
class PlayerAnswerViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = PlayerAnswerSerializer
    queryset = PlayerAnswer.objects.all()


# Sajjad
def popular_choices_help(question_id):
    choices = Choice.objects.filter(question_id=question_id).values('pk', 'chosen_count')
    return choices

# def second_chance_help():
#     pass
