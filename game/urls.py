from django.urls import path
from game.views import *

urlpatterns = [
    path('random-categories/', GenerateRandomCategoryView.as_view(), name='random_categories'),
    path('answer-question/', AnswerQuestionView.as_view(), name='answer_question'),
    path('random-questions/<int:pk>/', GenerateRandomQuestionView.as_view(), name='answer_question'),
    path('start-match/', StartMatchView.as_view(), name='start_match'),
]
