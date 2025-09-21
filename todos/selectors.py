from django.db.models.query import QuerySet
from typing import Optional
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Todo
from .filters import TodoFilter

def todo_list(*, filters = None) -> QuerySet[Todo]:
    filters = filters or {}
    
    base_qs = Todo.objects.all()
    
    return TodoFilter(filters, base_qs).qs

def todo_get(*, todo_pk : int) -> Optional[Todo]:
    try: 
        return get_object_or_404(Todo, pk=todo_pk)
    except Http404:
        return None
    
