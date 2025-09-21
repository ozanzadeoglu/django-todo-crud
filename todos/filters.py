import django_filters
from .models import Todo

class TodoFilter(django_filters.FilterSet):
    completed = django_filters.BooleanFilter()
    
    order_by = django_filters.OrderingFilter(
        fields=['created_at', 'updated_at']
    )

    class Meta:
        model = Todo
        fields = ["completed"]