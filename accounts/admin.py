from django.contrib import admin

from accounts.models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    list_editable = ['is_active']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'point', 'coin', 'reported_times', 'is_active']

    @staticmethod
    def is_active(obj):
        return obj.user.is_active


@admin.register(Admin)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'is_staff', 'is_superuser',
                    'is_active']

    @staticmethod
    def username(obj):
        return obj.user.username

    @staticmethod
    def first_name(obj):
        return obj.user.first_name

    @staticmethod
    def last_name(obj):
        return obj.user.last_name

    @staticmethod
    def is_staff(obj):
        return obj.user.is_staff

    @staticmethod
    def is_superuser(obj):
        return obj.user.is_superuser

    @staticmethod
    def is_active(obj):
        return obj.user.is_active
