from django.contrib import admin
from .models import Todo, IssueReport, Feedback

admin.site.register(Todo)
admin.site.register(IssueReport)
admin.site.register(Feedback)
