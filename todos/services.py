from .models import Todo
from django.db import transaction


@transaction.atomic
def todo_create(*, title: str, description: str, completed: bool = False) -> Todo:
    todo = Todo.objects.create(
        title=title, description=description, completed=completed
    )
    return todo


@transaction.atomic
def todo_update(*, todo: Todo, title = None, description = None, completed = None) -> Todo:
    #need to check generic solutions
    if title is not None:
        todo.title = title
    if description is not None:
        todo.description = description
    if completed is not None:
        todo.completed = completed

    todo.save()
    return todo


@transaction.atomic
def todo_delete(*, todo_pk: int) -> bool:
    deleted_count, _ = Todo.objects.filter(pk=todo_pk).delete()

    if deleted_count == 0:
        return False

    return True
