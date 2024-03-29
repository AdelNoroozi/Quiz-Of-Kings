from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Count, Sum
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

from accounts.models import Player, Admin


class Category(models.Model):
    name = models.CharField(max_length=25, verbose_name=_('category'))
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions',
                                 verbose_name=_('category'))
    text = models.TextField(verbose_name=_('question text'))
    answered_count = models.PositiveIntegerField(default=0, verbose_name=_('answered count'))
    created_by = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='questions',
                                   verbose_name=_('creator'),
                                   blank=True, null=True)
    confirmed_by = models.ForeignKey(Admin, on_delete=models.PROTECT, related_name='questions',
                                     verbose_name=_('confirmer'),
                                     blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name=_('creation date'))
    confirmed_at = models.DateField(verbose_name=_('confirmation date'), blank=True, null=True)
    likes = models.PositiveIntegerField(default=0, verbose_name=_('likes'))
    dislikes = models.PositiveIntegerField(default=0, verbose_name=_('dislikes'))

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.text

    def get_popular_choices(self):
        choices = Choice.objects.filter(question_id=self.id).values('pk', 'chosen_count')
        sum_count = choices.aggregate(s=Sum('chosen_count'))

        if not choices:
            response_data = {'detail': 'NOT found'}
            return Response(response_data)

        response = {'question_id': self.id}
        for choice in choices:
            if sum_count['s'] == 0:
                percent = 0
            else:
                percent = round((choice['chosen_count'] / sum_count['s']) * 100, 2)
            response[choice['pk']] = percent

        return Response(response)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name=_('question'))
    text = models.TextField(verbose_name=_('choice text'))
    chosen_count = models.PositiveIntegerField(default=0, verbose_name=_('chosen count'))
    is_correct = models.BooleanField(default=False, verbose_name=_('is correct'))

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')

    def __str__(self):
        return f'{self.question.text} - {self.text}'


class Match(models.Model):
    STATUSES = (('MM', 'matchmaking'),
                ('OG', 'ongoing'),
                ('F', 'finished'),
                ('Q', 'quited'))

    TURNS = (('S', 'starter'),
             ('J', 'joiner'))
    starter_player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='player_matches_as_starter',
                                       verbose_name=_('starter player'))
    joining_player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='player_matches_as_joiner',
                                       verbose_name=_('joining player'), blank=True, null=True)
    starter_player_score = models.PositiveIntegerField(default=0, verbose_name=_('starter player score'))
    joining_player_score = models.PositiveIntegerField(default=0, verbose_name=_('joining player score'))
    selected_categories = models.ManyToManyField(Category, blank=True, verbose_name=_('selected categories'))
    status = models.CharField(max_length=15, choices=STATUSES, verbose_name=_('status'), blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('creation time'))
    modified_at = models.DateTimeField(verbose_name=_('last modification'), blank=True, null=True)
    turn = models.CharField(max_length=10, choices=TURNS, default='S', verbose_name=_('turn'))
    expires_at = models.DateTimeField(verbose_name=_('expected expiring date'), blank=True, null=True)
    rounds_played = models.PositiveIntegerField(default=0, verbose_name=_('round_played'),
                                                validators=[MaxValueValidator(6)])

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')

    def __str__(self):
        if self.joining_player is None:
            return f'{self.starter_player.user.username} vs blank-user at {self.created_at}'
        else:
            return f'{self.starter_player.user.username} vs {self.joining_player.user.username} at {self.created_at}'


class PlayerAnswer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='player_answers',
                               verbose_name=_('player'))
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='player_answers', verbose_name=_('match'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='player_answers',
                                 verbose_name=_('question'))
    answer = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='player_answers')

    class Meta:
        verbose_name = _('Player Answer')
        verbose_name_plural = _('Player Answers')

    def __str__(self):
        if self.player == self.match.starter_player:
            return f'{self.player.user.username} - «{self.question.text}» : «{self.answer.text}» in match vs {self.match.joining_player} at «{self.match.created_at}»'
        else:
            return f'{self.player.user.username} - «{self.question.text}» : «{self.answer.text}» in match vs {self.match.starter_player} at «{self.match.created_at}»'
