from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(blank=True, null=True)
    important = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @property
    def get_class(self):
        if self.important:
            return "todo important"
        else:
            return "todo"


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"message from - {self.name}"


class IssueReport(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()

    def __str__(self):
        return f"report from - {self.name}"