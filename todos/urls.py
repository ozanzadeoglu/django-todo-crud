from django.urls import path
from . import views

urlpatterns = [
    path("todos/", views.TodoListApi.as_view(), name= "todo-list-create"),
    path("todos/<int:pk>/", views.TodoDetailApi.as_view(), name= "todo-detail"),
]
