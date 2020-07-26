from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='list_page'),
    path('update_todo/<str:pk>/', views.updateTodo, name='update_todo')
]
