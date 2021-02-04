from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Tasks
from .forms import TaskForm

# Create your views here.

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username, email, password)
            if not user.save():
                messages.success(request,f"User '{username}' is Successfully Registered!")
                return redirect("/")
            else:
                messages.error(request, f"Something Went Wrong")
        return render(request, 'signup.html', {"user_agent": request.user_agent})
    else:
        return redirect('dashboard')


def dashboard(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if(request.POST):
                task = request.POST['task']
                if(task):
                    name = request.user.username
                    form = TaskForm({'task': task, 'done': False, 'name': name})
                    if form.is_valid():
                        messages.success(request, f"task {task} is successfully added!")
                        form.save()
                        return redirect('/')
                else:
                    messages.error(request, f"please enter a name for the task")
                    return redirect('/')
        else:
            user = request.user.username
            user_tasks = Tasks.objects.all().filter(name=user)
            return render(request, 'dashboard.html', {'user_tasks': user_tasks, "user_agent": request.user_agent})
    else:
        return redirect('/')

def logout_user(request):
    if request.user.is_authenticated:
        messages.info(request, f"See you later {request.user.username}!")
        logout(request)
        return redirect('/')
    else:
        return redirect('/')

 # user = request.user.username
        # user_tasks = Tasks.objects.all().filter(name=user)
        # return render(request, 'dashboard.html', {'user_tasks': user_tasks})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['passwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}")
            user = request.user.username
            user_tasks = Tasks.objects.all().filter(name=user)
            return redirect('dashboard')
        else:
            messages.error(request, f"Invalid username or password!")
            return render(request, 'index.html', {"user_agent": request.user_agent})

    elif request.user.is_authenticated:
        user = request.user.username
        user_tasks = Tasks.objects.all().filter(name=user)
        return redirect('dashboard')
    return render(request, 'index.html', {"user_agent": request.user_agent})

def delete_task(request, task_id):
    task = Tasks.objects.get(pk=task_id)
    messages.success(request, f"task '{task.task}' deleted successfully!")
    task.delete()

    return redirect('dashboard')

def update_task(request, task_id):
    if request.method == "POST":
        task = Tasks.objects.get(pk=task_id)
        old_name = task.task
        task.task = request.POST['task']
        task.save()
        messages.success(request, f"task '{old_name}' was updated! to '{task.task}'")
        return redirect('dashboard')
    else:
        task = Tasks.objects.get(pk=task_id)
        return render(request, 'update.html', {'task': task, "user_agent": request.user_agent})

def set_task(request, task_id):
    task = Tasks.objects.get(pk=task_id)
    if(task.done):
        task.done = False
        messages.warning(request, f"task '{task.task}' set as not")
    else:
        task.done = True
        messages.success(request, f"task '{task.task}' set as done")
    task.save()

    return redirect('dashboard')
