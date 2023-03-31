from rest_framework import serializers

from accounts.serializers import PlayerSerializer
from game.serializers import QuestionMiniSerializer
from .models import LikeOrDislike


class LikeOrDislikeSerializer(serializers.ModelSerializer):
    user = PlayerSerializer(many=False, read_only=True)
    question = QuestionMiniSerializer(many=False, read_only=True)

    class Meta:
        model = LikeOrDislike
        fields = ('id', 'user', 'question', 'type')
        read_only_fields = ('id',)
