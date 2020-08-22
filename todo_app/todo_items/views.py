from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import datetime

from .models import Todo
from .forms import RegisterForm, LoginForm, TodoForm

now = datetime.datetime.today()
tomorrow_1 = datetime.date.today() + datetime.timedelta(days=1)
tomorrow_2 = datetime.date.today() + datetime.timedelta(days=2)
tomorrow_3 = datetime.date.today() + datetime.timedelta(days=3)
tomorrow_4 = datetime.date.today() + datetime.timedelta(days=4)
tomorrow_5 = datetime.date.today() + datetime.timedelta(days=5)
tomorrow_6 = datetime.date.today() + datetime.timedelta(days=6)
tomorrow_7 = datetime.date.today() + datetime.timedelta(days=7)



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
            'form':form,
            }
        
    return render(request, 'todo_items.html', context)


@login_required
def today(request):
    user = request.user
    todos = Todo.objects.filter(author=user)
    todos_today = Todo.objects.filter(created=now, author=user)
    form = TodoForm()

    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return redirect("")

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

    if request.method =='POST':
        
        form = TodoForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            form.save()
        return redirect('/seven_days')

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


def updateTodo(request, pk):
    user = request.user
    todo = Todo.objects.get(pk=pk)

    form = TodoForm(instance=todo)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            reminder_time = form.cleaned_data['reminder_time']
            reminder_hour = reminder_time[0:2]
            reminder_minute = reminder_time[3:5]
            if form.instance.daily_reminder == True:
                try:
                    periodic_task = PeriodicTask.objects.get(name='Reminder'+'_'+str(user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk))
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
                            name='Reminder'+'_'+str(user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk),
                            task='todo_items.tasks.send_email_task3',
                            )
                    except ValidationError:
                        PeriodicTask.objects.get(
                            crontab=schedule,
                            name='Reminder'+'_'+str(user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk),
                            task='todo_items.tasks.send_email_task3',
                            )
            if form.instance.daily_reminder == False:
                try:
                    periodic_task = PeriodicTask.objects.get(name='Reminder'+'_'+str(user)+'_'+str(reminder_hour)+':'+str(reminder_minute)+'_'+'id'+':'+str(todo.pk))
                    periodic_task.enabled = False
                    periodic_task.save()
                except:
                    pass
            return redirect("/")

    context = {'form':form, 'todo':todo}

    return render(request, 'update_todo_expand.html', context)


def deleteTodo(request, pk):
    item = Todo.objects.get(pk=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')


    context = {'item':item}
    return render(request, 'delete_todo.html', context)