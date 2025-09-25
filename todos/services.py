from .models import Todo
from django.db import transaction
from .utils import generate_todo_cache_key
from .selectors import todo_list
from django.core.cache import cache



@transaction.atomic
def todo_create(*, title: str, description: str, completed: bool = False) -> Todo:
    todo = Todo.objects.create(
        title=title, description=description, completed=completed
    )
    return todo


@transaction.atomic
def todo_update(*, todo: Todo, title=None, description=None, completed=None) -> Todo:
    # need to check generic solutions
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


def todo_list_cache(*, filters: dict, limit: int, offset: int) -> None:
    from .views import TodoListApi

    todo_qs = todo_list(filters=filters)

    total_count = todo_qs.count()
    paginated_todos = todo_qs[offset : offset + limit]

    serialized_data = TodoListApi.OutputSerializer(paginated_todos, many=True).data

    cached_response = {
        "limit": limit,
        "offset": offset,
        "count": total_count,
        "results": serialized_data,
    }

    cache_key = generate_todo_cache_key(filters, limit, offset)
    cache.set(cache_key, cached_response, timeout=10)
