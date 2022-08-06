from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from todo.models import Todo
from .serializers import TodoSerializer, TrashedTodoSerializer
from .pagination import TodoPagination
from rest_framework import status


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

@api_view
def create_todo(request):
    if request.method != 'POST':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    kwargs = {}
    kwargs['title'] = request.POST.get("title")
    kwargs['user'] = request.user
    description = request.POST.get("description", False)
    if bool(description):
        kwargs['description'] = description
    important = request.POST.get("important", False)
    if bool(important):
        kwargs['important'] = True
    return Response(kwargs)
