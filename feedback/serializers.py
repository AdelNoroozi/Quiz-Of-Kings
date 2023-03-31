from rest_framework import serializers
from .models import LikeOrDislike


class LikeOrDislikeSerializer(serializers.Serializer):
    user = serializers.CharField(source='user.user.username', read_only=True)
    question = serializers.CharField(source='question.text', read_only=True)

    class Meta:
        model = LikeOrDislike
        fields = ('id', 'user', 'question', 'type')
        read_only_fields = ('id',)
