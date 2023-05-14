from django.contrib import admin
from project.users.models import SendEmail


@admin.register(SendEmail)
class SendEmailAdmin(admin.ModelAdmin):
    pass
