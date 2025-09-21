from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.request import Request
from rest_framework.views import APIView

class TodoListApi(APIView):
    

    def get(self, request: Request):
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 2))
        
        offset = (page - 1) * page_size
        
        todos = Todo.objects.all()[offset: offset + page_size]
        total_count = Todo.objects.count()
        
        serializer = TodoSerializer(todos, many = True)
        
        return Response({
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size,
            "results": serializer.data
            })
        
    def post(self, request: Request):
        serializer = TodoSerializer(data = request.data)
        
        if(serializer.is_valid(raise_exception = True)):
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)


class TodoDetailApi(APIView):
    serializer_class = TodoSerializer
    
    def get(self, request: Request, pk):
        todo = get_object_or_404(Todo, pk = pk)
        serializer = self.serializer_class(todo)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    
    def put(self, request: Request, pk):
        todo = get_object_or_404(Todo, pk = pk)
        serializer = self.serializer_class(todo, data = request.data)
        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self, request: Request, pk):
        deleted_count, _ = Todo.objects.filter(pk = pk).delete()
        if deleted_count == 0:
            return Response(status= status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_204_NO_CONTENT)    
        