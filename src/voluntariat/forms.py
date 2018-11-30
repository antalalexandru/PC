from django import forms
from django.contrib.auth.forms import UserCreationForm

from voluntariat.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=250)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


