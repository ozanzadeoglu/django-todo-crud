from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer, TodoMinimalSerializer
from django.core.paginator import Paginator

# Create your views here.
@api_view(["GET", "POST"])
def todo_list_create(request):
    if request.method == "GET":
        
        page = request.GET.get("page")
        page_size = request.GET.get("page_size")
        
        if not page and not page_size:
            todos = Todo.objects.all()
            serializer = TodoSerializer(todos, many = True)
            return Response({
                "results" : serializer.data
            })
        
        page = int(page or 1)
        page_size = int(page_size or 2)
        
        offset = (page - 1) * page_size
        
        todos = Todo.objects.all()[offset:offset + page_size]
        total_count = Todo.objects.count()
        
        serializer = TodoSerializer(todos, many = True)
        
        return Response({
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size,
            "results": serializer.data
            })
    
    elif request.method == "POST":
        serializer = TodoSerializer(data = request.data)
        
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET", "PUT", "DELETE", "PATCH"])
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk = pk)
    
    if request.method == "GET":
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == "PATCH":
        serializer = TodoSerializer(todo, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    