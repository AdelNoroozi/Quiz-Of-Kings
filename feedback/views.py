from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Player
from game.models import Question
from .models import LikeOrDislike
from .serializers import LikeOrDislikeSerializer


class LikeOrDislikeView(APIView):
    def post(self, request):
        serializer = LikeOrDislikeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('unauthenticated')

            player = Player.objects.filter(user=user).first()
            if not player:
                response = {'detail': 'player NOT found!'}
                return Response(response)

            try:
                question_id = request.data['question']
                feedback_type = request.data['type']

            except Exception as e:
                response = {'detail': str(e)}
                return Response(response)

            question = Question.objects.filter(id=question_id).first()
            if not question:
                response = {'detail': 'question NOT found!'}
                return Response(response)

            if feedback_type == 'L' or feedback_type == 'D':
                try:
                    like_dislike = LikeOrDislike.objects.create(user=player, question=question, type=feedback_type)
                except Exception as e:
                    response = {'detail': str(e)}
                    return Response(response)

                if feedback_type == 'L':
                    question.likes += 1
                else:
                    question.dislikes += 1

                question.save()

                ser = LikeOrDislikeSerializer(like_dislike)
                return Response(ser.data)

            else:
                response = {'detail': 'invalid type!'}
                return Response(response)

        return Response(serializer.errors)
