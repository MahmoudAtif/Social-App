from django.contrib.auth.forms import UserCreationForm
from django import forms
from project.users.models import User

class CustomeUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)