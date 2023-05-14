from django.contrib import admin
from project.posts.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass