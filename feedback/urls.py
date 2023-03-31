from django.urls import path
from .views import LikeOrDislikeView

urlpatterns = [
    path('like-dislike/', LikeOrDislikeView.as_view(), name='like_dislike')
]
