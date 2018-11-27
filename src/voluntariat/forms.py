from django import forms
from .models import Event
from django.contrib.admin import  widgets


class EventForm(forms.ModelForm):
    start_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm"}))
    end_date = forms.DateTimeField(widget=forms.TextInput(attrs={"placeholder": "yyyy-mm-dd hh:mm"}))

    class Meta:
        model = Event
        fields = ('name', 'picture', 'location', 'description', 'benefits', 'start_date', 'end_date')
