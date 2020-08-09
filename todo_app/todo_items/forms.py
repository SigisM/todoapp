from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'created', 'completed']
        widgets = {
            'created': DateInput(),
        }

class LoginForm(forms.Form):

    fields = ['username', 'password']


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]