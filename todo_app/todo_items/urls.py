from django.urls import path
from . import views
# from .views import PostListView

urlpatterns = [
    path('', views.index, name='list_page'),
    path('register/', views.register, name='register_page'),
    path('update_todo/<str:pk>/', views.updateTodo, name='update_todo'),
    path('delete_todo/<str:pk>/', views.deleteTodo, name='delete_todo'),
]
