from django import forms
from django.contrib.auth.forms import UserCreationForm

from voluntariat.models import User, Event


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


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['personal_description']


class ChangePasswordForm(forms.Form):
    old_password_flag = True  # Used to raise the validation error when it is set to False
    old_password = forms.CharField(label="Old Password", max_length=32, widget=forms.PasswordInput)
    new_password = forms.CharField(label="New Password", max_length=32, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="Repeat Password", max_length=32, widget=forms.PasswordInput)

    def set_old_password_flag(self):

        # This method is called if the old password entered by user does not match the password in the database, which sets the flag to False

        self.old_password_flag = False

        return 0

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        repeat_password = self.cleaned_data.get('repeat_password')
        old_password = self.cleaned_data.get('old_password')
        self.old_password_flag = False

        if new_password != repeat_password:
            raise forms.ValidationError(
                {'repeat_password': ['the new password and the repeat password must be the same']})

        if new_password == old_password:
            raise forms.ValidationError(
                {'new_password': ['the new password must be different than the current password']})

        return self.cleaned_data

    def clean_old_password(self, *args, **kwargs):
        old_password = self.cleaned_data.get('old_password')
        if not self.old_password_flag:
            raise forms.ValidationError("The old password that you have entered is wrong.")
        return old_password
