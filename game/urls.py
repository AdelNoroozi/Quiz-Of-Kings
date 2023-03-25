from django.urls import path, include
from game.views import *
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
# router.register('questions', QuestionViewSet)
question_nested_router = NestedDefaultRouter(router, 'categories', lookup='category')
question_nested_router.register('questions', QuestionViewSet, basename='questions')
choice_nested_router = NestedDefaultRouter(question_nested_router, 'questions', lookup='question')
choice_nested_router.register('choices', ChoicesViewSet, basename='choices')
# router.register('choices', ChoicesViewSet)
router.register('player_answers', PlayerAnswerViewSet)
router.register('matches', MatchViewSet)

urlpatterns = [
    path('random-categories/', GenerateRandomCategoryView.as_view(), name='random_categories'),
    path('answer-question/', AnswerQuestionView.as_view(), name='answer_question'),
    path('start-match/', StartMatchView.as_view(), name='start_match'),
    path('', include(router.urls)),
    path('', include(question_nested_router.urls)),
    path('', include(choice_nested_router.urls)),
]
