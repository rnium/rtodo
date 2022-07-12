from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
import todo
from todo.models import Todo
from .serializers import TodoSerializer


class ActiveTodoView(ListCreateAPIView):
    serializer_class = TodoSerializer
    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user, complete=False, trashed=False).order_by('-added')
        return todos
