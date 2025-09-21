from .models import Todo
from django.db import transaction

@transaction.atomic
def todo_create(*, title: str, description: str, completed: bool = False) -> Todo:
    todo = Todo.objects.create(title = title, description = description, completed = completed)
    return todo