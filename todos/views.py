from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from common.pagination import get_paginated_response, LimitOffsetPagination
from todos.selectors import todo_list, todo_get
from todos.services import todo_create, todo_delete, todo_update
from .models import Todo
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework import serializers
from .tasks import todo_list_cache_task
from django.core.cache import cache
from .utils import generate_todo_cache_key


class TodoListApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Todo
            fields = [
                "id",
                "title",
                "description",
                "completed",
                "created_at",
                "updated_at",
            ]

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=200)
        description = serializers.CharField(allow_blank=True)
        completed = serializers.BooleanField(default=False)

    class FilterSerializer(serializers.Serializer):
        completed = serializers.BooleanField(required=False, allow_null=True)
        order_by = serializers.ChoiceField(
            choices=["created_at", "-created_at", "updated_at", "-updated_at"],
            required=False,
            default="-updated_at",
        )

    def get(self, request: Request):
        filter_serializer = self.FilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        todo_qs = todo_list(filters=filter_serializer.validated_data)

        limit = int(
            request.query_params.get("limit", LimitOffsetPagination.default_limit)
        )
        offset = int(request.query_params.get("offset", 0))

        next_offset = limit + offset

        cache_key = generate_todo_cache_key(
            filter_serializer.validated_data, limit, offset
        )

        cached_response = cache.get(cache_key)

        if cached_response is not None:
            todo_list_cache_task.delay(
            filters = filter_serializer.validated_data,
            limit = limit, 
            offset = next_offset
            )
            return Response(cached_response)
        response = get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=self.OutputSerializer,
            queryset=todo_qs,
            request=request,
            view=self,
        )
        todo_list_cache_task.delay(
            filters = filter_serializer.validated_data,
            limit = limit, 
            offset = next_offset
        )
        return response

    def post(self, request: Request):
        serializer = self.InputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            todo = todo_create(**serializer.validated_data)
            serialized_todo = self.OutputSerializer(todo).data
            return Response(serialized_todo, status=status.HTTP_201_CREATED)


class TodoDetailApi(APIView):
    # New serializer to handle partial updates
    class UpdateInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=200, required=False)
        description = serializers.CharField(allow_blank=True, required=False)
        completed = serializers.BooleanField(required=False)

    def get(self, request: Request, pk):
        todo = todo_get(todo_pk=pk)

        if todo is None:
            raise Http404

        serializer = TodoListApi.OutputSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk):
        todo = todo_get(todo_pk=pk)

        if todo is None:
            raise Http404

        serializer = self.UpdateInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            updated_todo = todo_update(todo=todo, **serializer.validated_data)

            serialized_updated_todo = TodoListApi.OutputSerializer(updated_todo).data
            return Response(serialized_updated_todo)

    def delete(self, request: Request, pk):
        is_deleted = todo_delete(todo_pk=pk)
        if is_deleted is False:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)
