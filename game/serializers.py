from rest_framework import serializers

from accounts.serializers import PlayerSerializer, AdminSerializer, PlayerMiniSerializer
from game.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'is_active')
        read_only_fields = ('id', 'is_active')


class ChoiceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id',)


class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    created_by = PlayerMiniSerializer(many=False, read_only=True)
    confirmed_by = AdminSerializer(many=False, read_only=True)
    choices = ChoiceMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            'id', 'category', 'text', 'choices', 'answered_count', 'created_by', 'confirmed_by', 'created_at',
            'confirmed_at', 'likes', 'dislikes')
        read_only_fields = ('id', 'answered_count', 'confirmed_by', 'created_at', 'confirmed_at', 'likes', 'dislikes')


class QuestionMiniSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = Question
        fields = ('id', 'category', 'text')
        read_only_fields = ('id',)


class ChoiceSerializer(serializers.ModelSerializer):
    question = QuestionMiniSerializer(many=False, read_only=True)

    class Meta:
        model = Choice
        fields = ('id', 'question', 'text', 'chosen_count', 'is_correct')
        read_only_fields = ('id', 'chosen_count')


class MatchSerializer(serializers.ModelSerializer):
    starter_player = PlayerMiniSerializer(many=False, read_only=True)
    joining_player = PlayerMiniSerializer(many=False, read_only=True)
    selected_categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = (
            'id', 'starter_player', 'joining_player', 'starter_player_score', 'joining_player_score',
            'selected_categories', 'status', 'created_at', 'modified_at', 'turn', 'expires_at', 'rounds_played')
        read_only_fields = (
            'id', 'starter_player_score', 'joining_player_score', 'status', 'created_at', 'modified_at', 'turn',
            'expires_at', 'rounds_played')


class MatchMiniSerializer(serializers.ModelSerializer):
    starter_player = PlayerMiniSerializer(many=False, read_only=True)
    joining_player = PlayerMiniSerializer(many=False, read_only=True)

    class Meta:
        model = Match
        fields = (
            'id', 'starter_player', 'joining_player', 'created_at')
        read_only_fields = ('id', 'created_at')


class CreateQuestionSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        category_id = self.context['category_id']
        question_text = self.validated_data['text']
        try:
            question_id = self.context['question_id']
            question = Question.objects.get(id=question_id)
            question.text = question_text
            question.save()
            self.instance = question
        except:
            self.instance = Question.objects.create(category_id=category_id, text=question_text)
        return self.instance

    class Meta:
        model = Question
        fields = ('id', 'text')


class CreateChoiceSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        question_id = self.context['question_id']
        choice_text = self.validated_data['text']
        is_correct = self.validated_data['is_correct']
        question_choices = Choice.objects.filter(question_id=question_id)
        if question_choices.filter(is_correct=True).exists() and is_correct:
            raise serializers.ValidationError('this question has already a correct answer')
        try:
            choice_id = self.context['choice_id']
            choice = Choice.objects.get(id=choice_id)
            choice.text = choice_text
            choice.is_correct = is_correct
            choice.save()
            self.instance = choice
        except:
            if question_choices.count() == 4:
                raise serializers.ValidationError('this question has already 4 answer')
            self.instance = Choice.objects.create(question_id=question_id, text=choice_text,
                                                  is_correct=is_correct)
        return self.instance

    class Meta:
        model = Choice
        fields = ('id', 'text', 'is_correct')


class PlayerAnswerSerializer(serializers.ModelSerializer):
    player = PlayerMiniSerializer(many=False, read_only=True)
    match = MatchMiniSerializer(many=False, read_only=True)
    question = QuestionMiniSerializer(many=False, read_only=True)
    answer = ChoiceMiniSerializer(many=False)
    result = serializers.BooleanField(source='answer.is_correct')

    class Meta:
        model = PlayerAnswer
        fields = ('player', 'match', 'question', 'answer', 'result')
        read_only_fields = ('id', 'result')
