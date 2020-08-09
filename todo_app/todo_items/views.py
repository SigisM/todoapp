from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
import datetime

from .models import *
from .forms import *


now = datetime.datetime.now()

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {"form":form})



def login(request):
    user_form = LoginForm()
    user = User()

    if request.method =='POST':
        user_form = LoginForm(request.POST)
        if user_form is not None:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user.is_active:
                login(request, user)
                return render(request, 'todo_items.html', {'form': user_form})
        else:
            return HttpResponse("Your account is disabled")
        
    return render(request, 'registration/login.html')


@login_required
def index(request):

    user = request.user
    todos = Todo.objects.filter(author=user)
    todos_today = Todo.objects.filter(created=now, author=user)
    todos_completed_before = Todo.objects.filter(completed=True, created__lt=now, author=user)
    todos_future = Todo.objects.filter(created__gt=now, author=user)
    todos_uncompleted_before = Todo.objects.filter(completed=False, created__lt=now, author=user)
    form = TodoForm()

    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
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