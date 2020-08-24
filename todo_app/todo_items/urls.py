from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list_page'),
<<<<<<< Updated upstream
    path('update_todo/<str:pk>/', views.updateTodo, name='update_todo'),
=======
    path('groups/', views.list_group, name='groups_page'),
    # path('groups_list/', views.group_list, name='groups_list'),
    path('today/', views.today, name='today_page'),
    path('seven_days/', views.seven_days, name='seven_days_page'),
    path('register/', views.register, name='register_page'),
    path('update_todo_expand/<str:pk>/', views.updateTodo, name='update_todo'),
>>>>>>> Stashed changes
    path('delete_todo/<str:pk>/', views.deleteTodo, name='delete_todo'),
]
