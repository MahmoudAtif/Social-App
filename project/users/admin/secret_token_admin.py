from django.contrib import admin
from project.users.models import SecretToken


@admin.register(SecretToken)
class SecretTokenAdmin(admin.ModelAdmin):
    pass
