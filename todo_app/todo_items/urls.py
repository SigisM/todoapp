from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic import TemplateView
# from django.conf.urls import (handler404, handler500)


urlpatterns = [
    path('', views.index, name='list_page'),
    path('groups/', views.create_delete_list_group, name='groups_page'),
    path('today/', views.today, name='today_page'),
    path('seven_days/', views.seven_days, name='seven_days_page'),
    path('register/', views.register, name='register_page'),
    path('settings/', views.user_settings, name='user_settings'),
    path('update_todo_expand/<str:pk>/', views.updateTodo, name='update_todo'),
    path('delete_todo/<str:pk>/', views.deleteTodo, name='delete_todo'),
    path('delete_reminder/<str:pk>/<str:reminder>', views.del_reminder, name="del_reminder"),
]
