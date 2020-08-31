from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from .models import *



class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'time'


class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['title', 'created', 'completed', 'daily_reminder', 'reminder_time', 'task_group', 'reminder_date', "custom_reminder"]
        widgets = {
            'created': DateInput(attrs={'class' : 'date_group'}),
            'title': forms.TextInput(attrs={'size': '40', 'class' : 'title_group', 'placeholder':" e.g. Arrange report"}),
            'reminder_time': DateTimeInput(format="%H:%M"),
            'reminder_date': DateInput,
            'task_group': forms.Select(attrs={'class' : 'task_group'})
        }


class LoginForm(forms.Form):

    fields = ['username', 'password']


class GroupForm(forms.ModelForm):

    class Meta:
        model = Todo_Group
        fields = ['group_name']
        widgets = {
            'group_name':forms.TextInput(attrs={'class' : 'group_name', 'size': '38', 'placeholder':"e.g. Travel"}),
        }


class RegisterForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            'username':forms.TextInput(attrs={'placeholder':"Your username"}),
            'email':forms.EmailInput(attrs={'placeholder':"Tasks reminders will be sent to this email"}),
        }
    

class SettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ['interval']
        widgets = {
            'interval':forms.NumberInput(attrs={'class' : 'settings_interval'})
        }