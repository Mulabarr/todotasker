from django.shortcuts import render, redirect

from tasker.models import Task

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User


def delete(task_id):
    Task.objects.delete(id=task_id)


def checker(*args):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in args:
        if i not in alphabet:
            return False
        else:
            return True


def register(request):
    if request.method == 'POST' and 'back' in request.POST:
        return redirect('start_page')
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username):
            User.objects.create_user(username=username, password=password)
            return redirect('start_page')
        else:
            return render(request, 'register.html', {'valid': 'This username in use'})
    if request.method == 'GET':
        return render(request, 'register.html', {})


def start_page(request):
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasker', username)
        else:
            return render(request, 'start_page.html',
                          {'valid': 'Your username or password is incorrect'})
    if request.method == 'POST' and 'reg' in request.POST:
        return redirect('register')

    if request.method == 'GET':
        logout(request)
        return render(request, 'start_page.html')


def tasker(request, username):
    if request.user.is_authenticated:
        if request.user.username == username:
            if request.method == 'GET':
                user = User.objects.get(username=username)
                user_id = user.id
                tasks = Task.objects.filter(user=user_id)
                if not tasks:
                    return render(request, 'task_page.html', {'valid': 'You have no tasks. Create new?'})
                return render(request, 'task_page.html', {'tasks': tasks})
            if request.method == 'POST' and 'complete' in request.POST:
                task = request.POST.get()
                task_id = task.id
                delete(task_id)
                return render(request, 'task_page.html', {})
            else:
                return redirect('start_page')
        else:
            logout(request)
            return redirect('start_page')
    else:
        return redirect('start_page')

