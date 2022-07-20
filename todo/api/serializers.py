from rest_framework.serializers import ModelSerializer
from todo.models import Todo

class TodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        exclude = ['trashed', 'complete', 'user']


class TrashedTodoSerializer(ModelSerializer):
    class Meta:
        model = Todo
        exclude = ['trashed', 'complete', 'completed', 'important', 'user']