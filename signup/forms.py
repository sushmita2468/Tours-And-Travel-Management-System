from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignupForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2', 'profile_picture', 'bio', 'contact_info', 'role')
