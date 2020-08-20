from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
# from django.forms import DateTimeField


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'time'


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'created', 'completed', 'daily_reminder', 'reminder_time']
        widgets = {
            'created': DateInput(),
            'title': forms.TextInput(attrs={'size': '40'}),
            'reminder_time': DateTimeInput(format="%H:%M"),
        }

class LoginForm(forms.Form):

    fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]