from django.contrib import admin

from game.models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active', ]
    list_filter = ['is_active', ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['category', 'text', 'answered_count', 'created_by', 'confirmed_by', 'likes', 'dislikes',
                    'is_active']
    list_editable = ['is_active', ]
    list_filter = ['confirmed_by', 'is_active']


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'chosen_count', 'is_correct']
    list_editable = ['is_correct', ]
    list_filter = ['is_correct', ]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['starter_player', 'joining_player', 'starter_player_score', 'joining_player_score', 'status',
                    'expires_at', 'rounds_played']
    list_filter = ['status', ]


@admin.register(PlayerAnswer)
class PlayerAnswerAdmin(admin.ModelAdmin):
    list_display = ['player', 'match', 'question', 'answer']
    list_filter = ['player', 'match', 'question']

