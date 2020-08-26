# Todo App
Powered by Django & Python

# The idea

This is a Todo App for your daily tasks.<br />
Constantly forgetting things on a rush? Write them once and you'll never forget things anymore!<br />
First Login with your SuperUser.<br />


# Installation

## Install Docker

Before running the server, install docker.

Latest version(not necessary):
### Linux
* [installing docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* [installing docker compose](https://docs.docker.com/compose/install/)

### Windows 10 Professional or Enterprise 64-bit (Get stable)
* [installing docker](https://hub.docker.com/editions/community/docker-ce-desktop-windows/)

### Windows 10 Home (At your own risk)
Normally, Docker is not meant to be installed on Windows Home edition since Home version of Windows don't support Hyper-V virtualization.<br />
Despite this there is a workaround. Use it at your own risk. Author of this app, by the way, uses Windows Home :)
* [installing docker](https://docs.docker.com/docker-for-windows/install-windows-home/#install-docker-desktop-on-windows-10-home)
* [workaround](https://itnext.io/install-docker-on-windows-10-home-d8e621997c1d)

## First steps

* Install [Pipenv](https://pypi.org/project/pipenv/) tool for easy living with virtual environments<br />
`$ pip install pipenv`

* Run virtual environment<br />
`$ pipenv shell`

* Install pipfile, pipfile.lock, requirements.txt at once<br />
`$ pipenv install`

* Check if all requirements are installed<br />
`$ pip list`

![Dependencies](img/pip_list.png?raw=true "Pip list")

Before starting the MySQL server you can configure *docker-compose.yml* file in the root folder of the project:<br />
**MYSQL_PASSWORD:** default is *admin*<br />
**MYSQL_ROOT_PASSWORD:** default is *admin*<br />
**ports:** default is *3308:3306*<br />

* Start MySQL server locally<br />
`$ docker-compose up -d`

* Start Redis broker on Docker to run Celery Tasks<br />
`$ docker run -d -p 6379:6379 redis`

* Make your first migrations<br />
`$ python manage.py migrate`

* Create SuperUser (admin)<br />
`$ python manage.py createsuperuser`

* List running docker containers<br />
`$ sudo docker ps`

You should see two running containers with their STATUS: UP
![Alt text](img/containers.png?raw=true "Container List")

* Run server<br />
`$ python manage.py runserver`

* Hop on [Localhost:8000](http://127.0.0.1:8000/) and you are ready to go<br />


# Instruction Manual

The App itself is self-explanatory, however there are two things for Celery Tasks and Periodic tasks to be working.

* Make sure you run the Celery Worker. Worker runs tasks scheduled by Celery Beat<br />
`$ celery -A todo_app worker --scheduler django --loglevel=info`

* Make sure you run the Celery Beat. Beat is a scheduller/planner itself<br />
`$ celery -A todo_app beat --scheduler django --loglevel=info`

By default Periodic tasks are schedulled twice a day (08:00 and 16:00 `timezone:'Europe/Vilnius'`).
Periodic tasks schedule may be changed or added in **celery.py** (dir where *settings.py* is)
```
from celery.task.schedules import crontab

app.conf.beat_schedule = {
    'any_name': {
        'task': 'proj.tasks.task_to_fire_name',
        'schedule': crontab(minute=0, hour=8, day_of_week="*"),
    },
    'any_name2': {
        'task': 'proj.task_to_fire_name2',
        'schedule': crontab(minute=0, hour=16, day_of_week="*"),
    },
}
```

Periodic tasks itself may be changed/added or deleted in **tasks.py** file of the app.
```
@app.task
def task_to_fire_name(args):
	print(args)
	return None

@app.task
def task_to_fire_name2(args):
	print(args)
	return None
```

# Links

[Celery](https://docs.celeryproject.org/en/stable/)<br />
[Django-Celery-Beat](https://django-celery-beat.readthedocs.io/en/latest/)<br />
