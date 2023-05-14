from django.contrib import admin
from project.posts.models import Share

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    pass