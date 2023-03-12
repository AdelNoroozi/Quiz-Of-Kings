from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Player, Admin


class Category(models.Model):
    name = models.CharField(max_length=25, verbose_name=_('category'))
    is_active = models.BooleanField(verbose_name=_('is active'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions',
                                 verbose_name=_('category'))
    text = models.TextField(verbose_name=_('question text'))
    answered_count = models.IntegerField(default=0, verbose_name=_('answered count'))
    created_by = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='questions',
                                   verbose_name=_('creation date'),
                                   blank=True, null=True)
    confirmed_by = models.ForeignKey(Admin, on_delete=models.PROTECT, related_name='questions',
                                     verbose_name=_('confirmation date'),
                                     blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name=_('creation date'))
    confirmed_at = models.DateField(auto_now_add=True, verbose_name=_('confirmation date'), blank=True, null=True)

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name=_('question'))
    text = models.TextField(verbose_name=_('choice text'))
    chosen_count = models.IntegerField(default=0, verbose_name=_('chosen count'))
    is_correct = models.BooleanField(default=False, verbose_name=_('is correct'))

    class Meta:
        verbose_name = _('Choice')
        verbose_name_plural = _('Choices')

    def __str__(self):
        return f'{self.question.text} - {self.text}'


class Match(models.Model):
    STATUSES = (('MM', 'matchmaking'),
                ('OG', 'ongoing'),
                ('F', 'finished'))
    TURNS = (('S', 'starter'),
             ('J', 'joiner'))
    starter_player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='player_matches_as_starter',
                                       verbose_name=_('starter player'))
    joining_player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='player_matches_as_joiner',
                                       verbose_name=_('joining player'), blank=True, null=True)
    starter_player_score = models.IntegerField(default=0, verbose_name=_('starter player score'))
    joining_player_score = models.IntegerField(default=0, verbose_name=_('joining player score'))
    status = models.CharField(max_length=15, choices=STATUSES, verbose_name=_('status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('creation time'))
    modificated_at = models.DateTimeField(verbose_name=_('last modification'), blank=True, null=True)
    turn = models.CharField(max_length=10, choices=TURNS, default='S', verbose_name=_('turn'))
    expires_at = models.DateTimeField(verbose_name=_('expected expiring date'))

    class Meta:
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')

    def __str__(self):
        return f'{self.starter_player.user.username} vs {self.joining_player.user.username} at {self.created_at}'
