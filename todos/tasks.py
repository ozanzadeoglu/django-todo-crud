from celery import shared_task
from .services import todo_list_cache


@shared_task
def todo_list_cache_task(*, filters: dict, limit: int, offset: int):
    
    todo_list_cache(filters=filters, limit=limit, offset=offset)
