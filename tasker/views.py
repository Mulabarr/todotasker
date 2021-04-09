from django.shortcuts import render, redirect

from tasker.models import Task

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User


def checker(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in word:
        if i not in alphabet:
            return False
        else:
            return True


def register(request):
    if request.method == 'POST' and 'back' in request.POST:
        return redirect('start_page')
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST.get('username')
        if checker(username) is not True:
            return render(request, 'register.html', {'valid': 'Incorrect username'})
        password = request.POST.get('password')
        if len(password) < 6 or checker(password) is not True:
            return render(request, 'register.html', {'valid': 'Incorrect password'})
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
    elif request.method == 'POST' and 'reg' in request.POST:
        return redirect('register')
    else:
        logout(request)
        return render(request, 'start_page.html')


def tasker(request, username):
    if request.user.is_authenticated:
        if request.user.username == username:
            user = request.user
            tasks = Task.objects.filter(user=user)
            tasks = list(tasks)
            if request.method == 'GET':
                if not tasks:
                    return render(request, 'task_page.html', {'valid': 'You have no tasks. Create new?'})
                return render(request, 'task_page.html', {'tasks': tasks})
            elif request.method == 'POST' and 'complete' in request.POST:
                return complete(request, user)
            else:
                return redirect('start_page')
        else:
            logout(request)
            return redirect('start_page')
    else:
        return redirect('start_page')


def create_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and 'back' in request.POST:
            return redirect('tasker')
        elif request.method == 'POST':
            new_task = request.POST.get('new_task')
            end_date = request.POST.get('new_date')
            user = request.user
            Task.objects.create(main_task=new_task, end_date=end_date, user=user)
            return redirect('tasker', username=request.user.username)
        else:
            return render(request, 'create_page.html')
    else:
        return redirect('start_page')


def complete(request, user):
    task = request.POST['task_id']
    task_id = int(task)
    all_task = Task.objects.get(id=task_id)
    all_task.delete()
    tasks = Task.objects.filter(user=user)
    if not tasks:
        return render(request, 'task_page.html', {'valid': 'You have no tasks. Create new?'})
    tasks = list(tasks)
    return render(request, 'task_page.html', {'tasks': tasks})

