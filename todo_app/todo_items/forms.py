from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'time'


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'created', 'completed', 'daily_reminder', 'reminder_time', 'task_group']
        widgets = {
            'created': DateInput(),
            'title': forms.TextInput(attrs={'size': '40'}),
            'reminder_time': DateTimeInput(format="%H:%M"),
            'task_group': forms.Select(attrs={'class' : 'task_group'})
        }

class LoginForm(forms.Form):

    fields = ['username', 'password']


class GroupForm(forms.ModelForm):

    class Meta:
        model = Todo_Group
        fields = ['group_name']
        widgets = {
            'group_name':forms.TextInput(attrs={'size': '40'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]