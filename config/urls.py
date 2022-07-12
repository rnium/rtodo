from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('api/', include('todo.api.urls')),
    path('todos/', views.current_todo, name="todos"),
    path('completed/', views.completed_todo, name="completed"),
    path('complete_todo/', views.complete_todo_api, name="complete_todo"),
    path('trash/', views.trashed_todo, name="trashed"),
    path('trash_todo/', views.trash_todo_api, name="trash_todo"),
    path('untrash_todo/', views.untrash_todo_api, name="untrash_todo"),
    path('delete_todo/', views.delete_todo_api, name="delete_todo"),
    path('create/', views.create_todo, name="create"),
    path('edit/<int:pk>', views.edit_todo, name="edit"),
    path('stats/', views.user_stat, name="stats"),
    path('login/', views.user_login, name="login"),
    path('signup/', views.signup_user, name="signup"),
    path('logout/', views.logout_user, name="logout"),
    path('sourcecode/', views.unavailable, name="sourcecode"),
    path('feedback/', views.feedback, name="feedback"),
    path('report/', views.report_issue, name="report"),
    path('rules/', views.unavailable, name="rules"),
    path('usermanual/', views.unavailable, name="usermanual"),
]

handler404 = 'todo.views.handler404'
