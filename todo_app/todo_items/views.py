from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import datetime

from .models import *
from .forms import *


now = datetime.datetime.now()

def index(request):
    todos = Todo.objects.all()
    todos_today = Todo.objects.filter(created=now)
    todos_completed_before = Todo.objects.filter(completed=True, created__lt=now)
    todos_future = Todo.objects.filter(created__gt=now)
    todos_uncompleted_before = Todo.objects.filter(completed=False, created__lt=now)
    form = TodoForm()

    if request.method =='POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')


    context = {'todos':todos,
            'todos_completed_before':todos_completed_before,
            'todos_future':todos_future,
            'todos_uncompleted_before':todos_uncompleted_before,
            'todos_today':todos_today,
            'form':form
            }
    
    return render(request, 'todo_items.html', context)


def updateTodo(request, pk):
    todo = Todo.objects.get(id=pk)

    form = TodoForm(instance=todo)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}

    return render(request, 'update_todo.html', context)


def deleteTodo(request, pk):
    item = Todo.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')


    context = {'item':item}
    return render(request, 'delete_todo.html', context)