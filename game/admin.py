from django.contrib import admin

from game.models import *

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Choice)
