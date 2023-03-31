from django.http import HttpRequest
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

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

            question_id = serializer.data['question']
            feedback_type = serializer.data['type']

            question = Question.objects.filter(id=question_id).first()
            if not question:
                response = {'detail': 'question NOT found!'}
                return Response(response)

            if feedback_type != 'L' or feedback_type != 'D':
                response = {'detail': 'invalid type!'}
                return Response(response)

            try:
                like_dislike = LikeOrDislike.objects.create(user=user, question=question, type=feedback_type)
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

        return Response(serializer.errors)
