from django.urls import path
from . import views
from django.conf.urls import url
from django.views.generic import TemplateView
# from .views import PostListView

urlpatterns = [
    path('', views.index, name='list_page'),
    path('groups/', views.list_group, name='groups_page'),
    # path('groups_list/', views.filteredView, name='groups_list'),
    path('groups/', views.list_group, name='groups_page'),
    path('today/', views.today, name='today_page'),
    path('seven_days/', views.seven_days, name='seven_days_page'),
    path('register/', views.register, name='register_page'),
    path('update_todo_expand/<str:pk>/', views.updateTodo, name='update_todo'),
    path('delete_todo/<str:pk>/', views.deleteTodo, name='delete_todo'),
]

