from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework
from todo.models import Todo
from .serializers import TodoSerializer, TrashedTodoSerializer
from .pagination import TodoPagination


class ActiveTodoView(ListCreateAPIView):
    serializer_class = TodoSerializer
    pagination_class = TodoPagination
    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user, complete=False, trashed=False).order_by('-added')
        return todos

class CompletedTodoView(ListAPIView):
    serializer_class = TodoSerializer
    pagination_class = TodoPagination
    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user, complete=True).order_by('-completed')
        return todos


class TrashedTodoView(ListAPIView):
    serializer_class = TrashedTodoSerializer
    pagination_class = TodoPagination
    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user, trashed=True).order_by('-added')
        return todos
