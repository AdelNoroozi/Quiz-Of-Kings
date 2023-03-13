from rest_framework import serializers

from accounts.serializers import PlayerSerializer, AdminSerializer, PlayerMiniSerializer
from game.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'is_active')
        read_only_fields = ('id',)


class ChoiceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    created_by = PlayerMiniSerializer(many=False)
    confirmed_by = AdminSerializer(many=False)
    choices = ChoiceMiniSerializer(many=True)

    class Meta:
        model = Question
        fields = (
            'id', 'category', 'text', 'choices', 'answered_count', 'created_by', 'confirmed_by', 'created_at',
            'confirmed_at', 'likes', 'dislikes')
        read_only_fields = ('id',)


class QuestionMiniSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = Question
        fields = ('id', 'category', 'text')
        read_only_fields = ('id',)


class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=False)

    class Meta:
        model = Choice
        fields = ('id', 'question', 'text', 'chosen_count', 'is_correct')
        read_only_fields = ('id',)


class MatchSerializer(serializers.ModelSerializer):
    starter_player = PlayerMiniSerializer(many=False)
    joining_player = PlayerMiniSerializer(many=False)
    selected_categories = CategorySerializer(many=True)

    class Meta:
        model = Match
        fields = (
            'id', 'starter_player', 'joining_player', 'starter_player_score', 'joining_player_score',
            'selected_categories', 'status', 'created_at', 'modified_at', 'turn', 'expires_at', 'rounds_played')
        read_only_fields = ('id',)


class MatchMiniSerializer(serializers.ModelSerializer):
    starter_player = PlayerMiniSerializer(many=False)
    joining_player = PlayerMiniSerializer(many=False)

    class Meta:
        model = Match
        fields = (
            'id', 'starter_player', 'joining_player', 'created_at')
        read_only_fields = ('id',)


class PlayerAnswerSerializer(serializers.ModelSerializer):
    player = PlayerMiniSerializer(many=False)
    match = MatchMiniSerializer(many=False)
    question = QuestionMiniSerializer(many=False)
    answer = ChoiceMiniSerializer(many=False)

    class Meta:
        model = PlayerAnswer
        fields = ('player', 'match', 'question', 'answer')
        read_only_fields = ('id',)