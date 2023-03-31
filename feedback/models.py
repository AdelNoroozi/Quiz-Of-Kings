from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import *
from game.models import Question


class ReportReason(models.Model):
    reason = models.TextField(verbose_name=_('reason'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    class Meta:
        verbose_name = _('Report Reason')
        verbose_name_plural = _('Report Reasons')

    def __str__(self):
        return self.reason


class Report(models.Model):
    STATUSES = (('S', 'submitted'),
                ('C', 'confirmed'),
                ('R', 'rejected'))
    user = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='reports', verbose_name=_('reporter'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reports', verbose_name=_('question'))
    reason = models.ForeignKey(ReportReason, on_delete=models.RESTRICT, related_name='reports',
                               verbose_name=_('reason'))
    admin = models.ForeignKey(Admin, on_delete=models.PROTECT, related_name='reports', verbose_name=_('admin'),
                              blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('creation date'))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('modification date'), blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUSES, verbose_name=_('status'), default='S')

    class Meta:
        verbose_name = _('Report')
        verbose_name_plural = _('Reports')

    def __str__(self):
        return f'{self.user.user.username} - {self.question.text}'


class LikeOrDislike(models.Model):
    TYPE = (('L', 'like'),
            ('D', 'dislike'))

    user = models.ForeignKey(Player, on_delete=models.PROTECT, related_name='like_dislike',
                             verbose_name=_('like / dislike'))
    type = models.CharField(choices=TYPE, max_length=2, verbose_name=_('type'), blank='L')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='like_dislike',
                                 verbose_name=_('question'))

    class Meta:
        verbose_name = _('Like Or Dislike')
        verbose_name_plural = _('Likes Or Dislikes')

    def __str__(self):
        return f'{self.user.user.username} - {self.question.text} - {self.type}'
