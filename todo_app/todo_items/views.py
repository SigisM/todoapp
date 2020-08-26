from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
import datetime
import json

from .models import Todo, Todo_Group
from .forms import RegisterForm, LoginForm, TodoForm, GroupForm


@receiver(post_save, sender=User)
def create_default_group(sender, instance, **kwargs):
    group_name = "Uncategorised"
    if Todo_Group.objects.filter(group_name=group_name, user=instance).exists():
        return False
    else:
        Todo_Group.objects.create(group_name=group_name, user=instance)


def set_default_group(request):
    todos = Todo.objects.filter(author=request.user)
    category = Todo_Group.objects.get(user=request.user, group_name = "Uncategorised")
    for todo in todos:
        if not todo.task_group:
            todo.task_group = category
            todo.save()



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


def is_valid_queryparam(param):
    return param !="" and param is not None


@login_required
def create_delete_list_group(request, **kwargs):
    form = GroupForm()
    qs = Todo.objects.filter(author=request.user)
    categories = Todo_Group.objects.filter(user=request.user)
    category = request.GET.get('category')

    if is_valid_queryparam(category):
        qs = qs.filter(task_group__group_name__icontains = category)

    if request.method =='POST':
        if 'createGroup' in request.POST:
            form = GroupForm(request.POST)
            form.instance.user = request.user
            if form.is_valid():
                group_name = form.cleaned_data['group_name']
                if Todo_Group.objects.filter(group_name=group_name, user=request.user).exists():
                    error_message = "Group name already exists!"
                    context = {'form': form,
                            'error_message': error_message,
                            'queryset':qs,
                            'categories':categories,
                            'category':category,
                        }
                    return render(request, 'group_list.html', context)
                else:
                    form.save()
                    form = GroupForm()
                    success_message = "Group sucessfully created!"
                    context = {'form': form,
                            'success_message': success_message,
                            'queryset':qs,
                            'categories':categories,
                            'category':category,
                        }

                    return render(request, 'group_list.html', context)

        elif 'deleteGroup' in request.POST:
            form = GroupForm(request.POST)
            form.instance.user = request.user
            if form.is_valid():
                item = form.cleaned_data['group_name']
                cat_to_delete = Todo_Group.objects.filter(user=request.user)
                if item == "Uncategorised":
                    form = GroupForm()
                    forbid_message = "Group 'Uncategorised' is a default group, thus it cannot be deleted"
                    context = {'form': form,
                            'forbid_message': forbid_message,
                            'queryset':qs,
                            'categories':categories,
                            'category':category,
                        }
                    return render(request, 'group_list.html', context)

                if cat_to_delete.filter(group_name=item).exists():
                    cat_to_delete.filter(group_name=item).delete()
                    form = GroupForm()
                    success_message = "Group sucessfully deleted!"
                    set_default_group(request)
                    context = {'form': form,
                            'success_message': success_message,
                            'queryset':qs,
                            'categories':categories,
                            'category':category,
                        }
                    return render(request, 'group_list.html', context)
                else:
                    error_message = "Group name does not exist!"
                    context = {'form': form,
                            'error_message': error_message,
                            'queryset':qs,
                            'categories':categories,
                            'category':category,
                        }
                    return render(request, 'group_list.html', context)


    context = {'form': form,
            'queryset':qs,
            'categories':categories,
            'category':category,
        }

    return render(request, 'group_list.html', context)


@login_required
def index(request):
    todos_today = Todo.objects.filter(created=datetime.datetime.today(), author=request.user)
    todos_completed_before = Todo.objects.filter(completed=True, created__lt=datetime.datetime.today(), author=request.user)
    todos_future = Todo.objects.filter(created__gt=datetime.datetime.today(), author=request.user)
    todos_uncompleted_before = Todo.objects.filter(completed=False, created__lt=datetime.datetime.today(), author=request.user)
    form = TodoForm()
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=request.user)
    
    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'todos_completed_before':todos_completed_before,
            'todos_future':todos_future,
            'todos_uncompleted_before':todos_uncompleted_before,
            'todos_today':todos_today,
            'form':form,
            }
        
    return render(request, 'todo_items.html', context)


@login_required
def today(request):
    todos_today = Todo.objects.filter(created=datetime.datetime.today(), author=request.user)
    form = TodoForm()
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=request.user)

    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.path)

    context = {'todos_today':todos_today,
            'form':form,
            }
        
    return render(request, 'today_items.html', context)


@login_required
def seven_days(request):
    todos_today = Todo.objects.filter(created=datetime.datetime.today(), author=request.user)
    todos_tomorrow_1 = Todo.objects.filter(created=(datetime.date.today() + datetime.timedelta(days=1)), author=request.user)
    todos_tomorrow_2 = Todo.objects.filter(created=(datetime.date.today() + datetime.timedelta(days=2)), author=request.user)
    todos_tomorrow_3 = Todo.objects.filter(created=(datetime.date.today() + datetime.timedelta(days=3)), author=request.user)
    todos_tomorrow_4 = Todo.objects.filter(created=(datetime.date.today() + datetime.timedelta(days=4)), author=request.user)
    todos_tomorrow_5 = Todo.objects.filter(created=(datetime.date.today() + datetime.timedelta(days=5)), author=request.user)
    todos_tomorrow_6 = Todo.objects.filter(created=(datetime.date.today() + datetime.timedelta(days=6)), author=request.user)
    form = TodoForm()
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=request.user)

    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(request.path_info)

    context = {'todos_today':todos_today,
            'todos_tomorrow_1':todos_tomorrow_1,
            'todos_tomorrow_2':todos_tomorrow_2,
            'todos_tomorrow_3':todos_tomorrow_3,
            'todos_tomorrow_4':todos_tomorrow_4,
            'todos_tomorrow_5':todos_tomorrow_5,
            'todos_tomorrow_6':todos_tomorrow_6,
            'form':form,
            }
        
    return render(request, '7days_items.html', context)


def updateTodo(request, pk):
    todo = Todo.objects.get(pk=pk)

    form = TodoForm(instance=todo)
    form.fields['task_group'].queryset = Todo_Group.objects.filter(user=request.user)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            reminder_time = form.cleaned_data['reminder_time']
            reminder_hour = reminder_time[0:2]
            reminder_minute = reminder_time[3:5]
            if form.instance.daily_reminder == True:
                try:
                    periodic_task = PeriodicTask.objects.get(name='Reminder'+'_'+str(request.user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk))
                    periodic_task.enabled = True
                    periodic_task.save()
                except:
                    schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute=int(reminder_minute),
                        hour=int(reminder_hour),
                        day_of_week='*',
                        day_of_month='*',
                        month_of_year='*',
                        timezone='Europe/Vilnius',
                        )
                    try: 
                        PeriodicTask.objects.create(
                            crontab=schedule,
                            name='Reminder'+'_'+str(request.user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk),
                            task='todo_items.tasks.one_off_task_reminder',
                            args=json.dumps([title, 'This is a reminder for your task!', request.user.email]),
                            one_off=True,
                            )
                    except ValidationError:
                        PeriodicTask.objects.get(
                            crontab=schedule,
                            name='Reminder'+'_'+str(request.user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk),
                            task='todo_items.tasks.one_off_task_reminder',
                            args=json.dumps([title, 'This is a reminder for your task!', request.user.email]),
                            one_off=True,
                            )
            if form.instance.daily_reminder == False:
                try:
                    periodic_task = PeriodicTask.objects.get(name='Reminder'+'_'+str(request.user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk))
                    periodic_task.enabled = False
                    periodic_task.save()
                except:
                    pass
            return HttpResponseRedirect("/")

    context = {'form':form, 'todo':todo}

    return render(request, 'update_todo_expand.html', context)


def deleteTodo(request, pk):
    item = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')


    context = {'item':item}
    return render(request, 'delete_todo.html', context)