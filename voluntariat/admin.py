from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from voluntariat.models import User,Event

admin.site.register(User, UserAdmin)
admin.site.register(Event)
