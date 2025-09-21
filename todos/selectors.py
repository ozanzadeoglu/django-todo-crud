from django.db.models.query import QuerySet

from .models import Todo
from .filters import TodoFilter

def todo_list(*, filters = None) -> QuerySet[Todo]:
    filters = filters or {}
    
    base_qs = Todo.objects.all()
    
    return TodoFilter(filters, base_qs).qs