from django.urls import path, include
from game.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('questions', QuestionViewSet)
router.register('choices', ChoicesViewSet)
router.register('player_answers', PlayerAnswerViewSet)
router.register('matches', MatchViewSet)

urlpatterns = [
    path('random-categories/', GenerateRandomCategoryView.as_view(), name='random_categories'),
    path('answer-question/', AnswerQuestionView.as_view(), name='answer_question'),
    path('start-match/', StartMatchView.as_view(), name='start_match'),
    path('', include(router.urls)),
]
