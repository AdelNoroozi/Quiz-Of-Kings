from django.urls import path
from game.views import *

urlpatterns = [
    path('random_categories/', GenerateRandomCategoryView.as_view(), name='random_categories'),
]
