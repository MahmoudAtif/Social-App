from django.contrib import admin
from project.friends.models import FriendList

@admin.register(FriendList)
class FriendListAdmin(admin.ModelAdmin):
    pass