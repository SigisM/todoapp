from django import forms

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