from django.contrib import admin
from project.posts.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass