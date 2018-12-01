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

class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm"}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm"}))

    class Meta:
        model = Event
        fields = ('name', 'picture', 'location', 'description', 'benefits', 'start_date', 'end_date')
