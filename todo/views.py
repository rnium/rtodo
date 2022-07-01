from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from datetime import date
from .models import Todo, Feedback, IssueReport
from django.core.paginator import Paginator
from django.utils import timezone
from .utils import get_paginator_context
from django.http import HttpResponse, JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import json


def home(request):
    if request.user.is_authenticated:
        return redirect('todos')
    else:
        return render(request, 'todo/home.html')


@login_required
def current_todo(request):
    context = {}
    todos = Todo.objects.filter(user=request.user, complete=False, trashed=False).order_by('-added')
    context['todos'] = todos
    context['username'] = request.user.username
    context['num_todos'] = len(todos)
    return render(request, 'todo/current.html', context=context)

@login_required
def completed_todo(request):
    context = {}
    todos = Todo.objects.filter(user=request.user, complete=True).order_by('-completed')
    paginator = Paginator(todos, 5)
    todos_page = paginator.get_page(request.GET.get('page'))
    context['username'] = request.user.username
    context['todos'] = todos_page
    context['num_todos'] = len(todos)
    context['paginator'] = get_paginator_context(todos_page)
    return render(request, 'todo/completed.html', context=context)


@login_required
def trashed_todo(request):
    context = {}
    context['username'] = request.user.username
    todos = Todo.objects.filter(user=request.user, trashed=True).order_by('-added')
    context['todos'] = todos
    return render(request, 'todo/trashed.html', context=context)


@login_required
def create_todo(request):
    if request.method == "GET":
        context = {}
        context['username'] = request.user.username
        return render(request, "todo/create.html", context=context)
    else:
        kwargs = {}
        kwargs['user'] = request.user
        kwargs['title'] = request.POST.get('title')
        description = request.POST.get('description')
        if bool(description):
            kwargs['description'] = description
        important = request.POST.get('important')
        if bool(important):
            kwargs['important'] = True
        Todo.objects.create(**kwargs)
        return redirect('todos')


@login_required
def edit_todo(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return HttpResponse('Non existing todo cannot be updated')
    if request.method == "GET":
        if todo.user != request.user:
            return HttpResponse('Unauthorized')
        else:
            context = {}
            context['username'] = request.user.username
            context['todo'] = todo
            return render(request, 'todo/update.html', context=context)
    else:
        todo.title = request.POST.get('title')
        description = request.POST.get('description')
        if bool(description):
            todo.description = description
        important = request.POST.get('important')
        if bool(important):
            todo.important = True
        else:
            todo.important = False
        todo.save()
        return redirect('todos')


def complete_todo_api(request):
    if request.method == 'GET':
        return HttpResponse("method not allowed")
    else:
        data = json.loads(request.body)
        try:
            todo = Todo.objects.get(pk=data['id'])
        except Todo.DoesNotExist:
            response = JsonResponse("invalid todo id", safe=False)
            response.status_code = 404
            return response
        if todo.user != request.user:
            response = JsonResponse("unauthorized", safe=False)
            response.status_code = 403
            return response

        todo.complete = True
        todo.completed = timezone.now()
        todo.save()
        return JsonResponse('updated', safe=False)


def trash_todo_api(request):
    if request.method == 'GET':
        return HttpResponse("method not allowed")
    else:
        data = json.loads(request.body)
        try:
            todo = Todo.objects.get(pk=data['id'])
        except Todo.DoesNotExist:
            response = JsonResponse("invalid todo id", safe=False)
            response.status_code = 404
            return response
        if todo.user != request.user:
            response = JsonResponse("unauthorized", safe=False)
            response.status_code = 403
            return response

        todo.trashed = True
        todo.save()
        return JsonResponse('updated', safe=False)


def untrash_todo_api(request):
    if request.method == 'GET':
        return HttpResponse("method not allowed")
    else:
        data = json.loads(request.body)
        try:
            todo = Todo.objects.get(pk=data['id'])
        except Todo.DoesNotExist:
            response = JsonResponse("invalid todo id", safe=False)
            response.status_code = 404
            return response
        if todo.user != request.user:
            response = JsonResponse("unauthorized", safe=False)
            response.status_code = 403
            return response

        todo.trashed = False
        todo.save()
        return JsonResponse('updated', safe=False) 


def delete_todo_api(request):
    if request.method == 'GET':
        return HttpResponse("method not allowed")
    else:
        data = json.loads(request.body)
        try:
            todo = Todo.objects.get(pk=data['id'])
        except Todo.DoesNotExist:
            response = JsonResponse("invalid todo id", safe=False)
            response.status_code = 404
            return response
        if todo.user != request.user:
            response = JsonResponse("unauthorized", safe=False)
            response.status_code = 403
            return response
        todo.delete()
        return JsonResponse('deleted', safe=False) 

@login_required
def user_stat(request):
    context = {}
    user = request.user
    context['username'] = user.username
    context['active_todos'] = Todo.objects.filter(user=user, complete=False, trashed=False).count()
    print(context['active_todos'])
    context['total_todos'] = Todo.objects.filter(user=user).count()
    context['completed_todos'] = Todo.objects.filter(user=user, complete=True).count()
    context['trashed_todos'] = Todo.objects.filter(user=user, trashed=True).count()
    today = date.today()
    context['today_added_todos'] = Todo.objects.filter(user=user, added__date=today).count()
    context['today_completed_todos'] = Todo.objects.filter(user=user, complete=True, completed__date=today).count()
    try:
        last_completed_todo = Todo.objects.filter(user=user, complete=True).latest('completed')
        context['last_completed'] = last_completed_todo.title
        context['last_completed_time'] = last_completed_todo.completed
    except Todo.DoesNotExist:
        context['last_completed'] = "N/A"
    return render(request, 'todo/stat.html', context=context)


@login_required
def logout_user(request):
   logout(request)
   return redirect('home') 


def user_login(request):
    if request.method == 'GET':
        return render(request, 'todo/login.html')
    else:
        data = request.POST
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            return redirect('todos')
        else:
            return render(request, 'todo/login.html', context={'error':'invalid credentials'})


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                user = User.objects.create(username=username)
            except IntegrityError:
                return render(request, 'todo/signup.html', context={'error': 'username not available', 
                                                                    'prev_values': True, 
                                                                    'username': username,
                                                                    'password1': password1,
                                                                    'password2': password2})
            user.set_password(password1)
            user.save()
            login(request, user)
            return redirect('todos')
        else:
            return render(request, 'todo/signup.html', context={'error': 'passwords mismatch', 
                                                                'prev_values': True, 
                                                                'username': username,
                                                                'password1': password1,
                                                                'password2': password2})


def unavailable(request):
    context = dict()
    context['logged_in'] = request.user.is_authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
    return render(request, 'todo/unavailable.html', context=context)


def feedback(request):
    context = {}
    context['logged_in'] = request.user.is_authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
    if request.method == "GET":
        return render(request, 'todo/feedback.html', context=context)
    else:
        name = request.POST.get('name', 'BlankName')
        feedback = request.POST.get('feedback', 'Blank message')
        message = Feedback.objects.create(name=name, message=feedback)
        message.save()
        context['response'] = "Feedback Receieved"
        return render(request, 'todo/feedback_response.html', context=context)


def report_issue(request):
    context = {}
    context['logged_in'] = request.user.is_authenticated
    if request.user.is_authenticated:
        context['username'] = request.user.username
    if request.method == "GET":
        return render(request, 'todo/issuereport.html', context=context)
    else:
        report_kwargs = {}
        report_kwargs['name'] = request.POST.get('name', 'BlankName')
        email = request.POST.get('email', False)
        if email:
            report_kwargs['email'] = email
        report_kwargs['message'] = request.POST.get('issue_text', 'Blank message')
        issue = IssueReport.objects.create(**report_kwargs)
        issue.save()
        context['response'] = "Issue Submitted"
        return render(request, 'todo/feedback_response.html', context=context)