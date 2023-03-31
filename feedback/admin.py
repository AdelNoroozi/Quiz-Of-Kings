from django.contrib import admin
from .models import *


@admin.register(LikeOrDislike)
class LikeOrDislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'type']
    list_filter = ['type']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'reason', 'admin', 'status']
    list_editable = ['status', ]
    list_filter = ['status', ]


@admin.register(ReportReason)
class ReportReasonAdmin(admin.ModelAdmin):
    list_display = ['reason', 'is_active']
    list_editable = ['is_active', ]
    list_filter = ['is_active', ]
