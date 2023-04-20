from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "name"]

class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "bio", "image"]

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password' )

