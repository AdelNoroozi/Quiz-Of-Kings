from django.contrib import admin

from accounts.models import *

admin.site.register(User)
admin.site.register(Player)
admin.site.register(Admin)
