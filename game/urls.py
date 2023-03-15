from django.urls import path
from game.views import *

urlpatterns = [
    path('random_categories/', GenerateRandomCategoryView.as_view(), name='random_categories'),
    path('answer_question/', AnswerQuestionView.as_view(), name='answer_question'),
]
