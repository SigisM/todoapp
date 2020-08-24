from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
import datetime

from .models import *
from .forms import *


now = datetime.datetime.now()

<<<<<<< Updated upstream
=======
@receiver(post_save, sender=User)
def create_default_group(sender, instance, **kwargs):
    group_name = "Uncategorised"
    if Todo_Group.objects.filter(group_name=group_name, user=instance).exists():
        return False
    else:
        Todo_Group.objects.create(group_name=group_name, user=instance)


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
>>>>>>> Stashed changes
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


<<<<<<< Updated upstream
=======
@login_required
def group_list(request):
    todos = Todo.objects.all()
    form = TodoForm()
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=request.user)

    if request.method =='POST':
        form = TodoForm(request.POST)
    context = {'todos':todos,
            'form':form,
            }

    return render(request, 'group_filter.html', context)


@login_required
def list_group(request):
    groups = Todo_Group.objects.all()
    form = GroupForm()

    if request.method =='POST':
        form = GroupForm(request.POST)
        form.instance.user = request.user
        if form.is_valid():
            group_name = form.cleaned_data['group_name']
            if Todo_Group.objects.filter(group_name=group_name, user=request.user).exists():
                error_message = "Group name already exists!" 
                return render(request, 'group_list.html', {'form': form, 'error_message': error_message})
            else:
                form.save()
                form = GroupForm()
                success_message = "Group sucessfully created!"

            return render(request, 'group_list.html', {'form': form, 'success_message': success_message})

    context = {'groups':groups,
            'form':form,
            }

    return render(request, 'group_list.html', context)



@login_required
def today(request):
    user = request.user
    todos = Todo.objects.filter(author=user)
    todos_today = Todo.objects.filter(created=now, author=user)
    form = TodoForm()
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=user)

    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.path)

    context = {'todos':todos,
            'todos_today':todos_today,
            'form':form,
            }
        
    return render(request, 'today_items.html', context)


@login_required
def seven_days(request):
    user = request.user
    todos = Todo.objects.filter(author=user)
    todos_today = Todo.objects.filter(created=now, author=user)
    todos_tomorrow_1 = Todo.objects.filter(created__gt=now, created__lt=tomorrow_2, author=user)
    todos_tomorrow_2 = Todo.objects.filter(created__gt=tomorrow_1, created__lt=tomorrow_3, author=user)
    todos_tomorrow_3 = Todo.objects.filter(created__gt=tomorrow_2, created__lt=tomorrow_4, author=user)
    todos_tomorrow_4 = Todo.objects.filter(created__gt=tomorrow_3, created__lt=tomorrow_5, author=user)
    todos_tomorrow_5 = Todo.objects.filter(created__gt=tomorrow_4, created__lt=tomorrow_6, author=user)
    todos_tomorrow_6 = Todo.objects.filter(created__gt=tomorrow_5, created__lt=tomorrow_7, author=user)
    form = TodoForm()
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=user)

    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.path_info)

    context = {'todos':todos,
            'todos_today':todos_today,
            'todos_tomorrow_1':todos_tomorrow_1,
            'todos_tomorrow_2':todos_tomorrow_2,
            'todos_tomorrow_3':todos_tomorrow_3,
            'todos_tomorrow_4':todos_tomorrow_4,
            'todos_tomorrow_5':todos_tomorrow_5,
            'todos_tomorrow_6':todos_tomorrow_6,
            'form':form,
            'tomorrow1':tomorrow_1,
            'tomorrow2':tomorrow_2,
            'tomorrow3':tomorrow_3,
            'tomorrow4':tomorrow_4,
            'tomorrow5':tomorrow_5,
            'tomorrow6':tomorrow_6,
            'now':now,
            }
        
    return render(request, '7days_items.html', context)


>>>>>>> Stashed changes
def updateTodo(request, pk):
    todo = Todo.objects.get(id=pk)

    form = TodoForm(instance=todo)
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=request.user)

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