from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
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
    # start_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm"}))

    #start_date = forms.DateField(
    #    widget=DateTimePickerInput(format='%Y')
    #)

    # end_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm"}))



    class Meta:
        model = Event
        fields = ('name', 'picture', 'location', 'description', 'benefits', 'start_date', 'end_date')
        widgets = {
            'start_date': DateTimePickerInput(format='%Y-%m-%d %H:%M'),
            'end_date': DateTimePickerInput(format='%Y-%m-%d %H:%M'),
        }

'''
        # start_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm", 'class': 'datetime-input'}))

        start_date = forms.DateField(
            widget=DateTimePickerInput(format='%Y-%m-%d %H:%M')
        )

        end_date = forms.DateField(
            widget=DateTimePickerInput(format='%Y-%m-%d %H:%M')
        )

        # end_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm"}))

        class Meta:
            model = Event
            fields = ('name', 'picture', 'location', 'description', 'benefits', 'start_date', 'end_date')

            widgets = {
                'start_date': DatePickerInput(format='%m/%d%Y'),  # python date-time format
                'end_date': DatePickerInput(
                    options={
                        "format": "YYYY-MM-DD HH:mm",  # moment date-time format
                    }
                ),
            }
            '''

class UserForm(forms.ModelForm):
    picture = forms.ImageField(label='Fotografia de  profil', required=False,
                               error_messages={'invalid': "Image files only"}, widget=forms.FileInput)
    personal_description = forms.CharField(label='Descriere', required=False, widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['picture', 'personal_description']

    def clean(self):
        personal_description = self.cleaned_data.get('personal_description')
        if 'pula' in personal_description or 'pizda' in personal_description or 'sugi' in personal_description:
            raise forms.ValidationError(
                {'personal_description': ['Incearca sa folosesti un limbaj adecvat.']})


class ChangePasswordForm(forms.Form):
    old_password_flag = True  # Used to raise the validation error when it is set to False
    old_password = forms.CharField(label="Parola veche", max_length=32, widget=forms.PasswordInput)
    new_password = forms.CharField(label="Parola noua", max_length=32, widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="Repeta parola", max_length=32, widget=forms.PasswordInput)

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
                {'repeat_password': ['Cele doua parole trebuie sa fie identice.']})

        if new_password == old_password:
            raise forms.ValidationError(
                {'new_password': ['Parola noua trebuie sa fie diferita fata de parola veche.']})

        return self.cleaned_data

    def clean_old_password(self, *args, **kwargs):
        old_password = self.cleaned_data.get('old_password')
        if not self.old_password_flag:
            raise forms.ValidationError("Parola veche pe care ai introdus-o este gresita.")
        return old_password
