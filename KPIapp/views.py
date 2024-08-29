import math
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect

from KPIapp.forms import UserForm, TaskForm, DepartmentForm, UserEditForm, EditTaskForm
from KPIapp.models import User, Tasks, TasksAnswers, Role, Notifications, Departments


# Create your views here.
@login_required(login_url='signIn')
def employee(request):
    return render(request, 'KPIapp/Employee/employee.html')


def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    return render(request, 'KPIapp/user_profile.html', context)


@login_required(login_url='signIn')
def supervisor(request):
    users = User.objects.all()
    tasks = Tasks.objects.all()
    departments = Departments.objects.all()

    tasks_new = Tasks.objects.filter(status='NEW')
    tasks_in_progress = Tasks.objects.filter(status='IN_PROGRESS')
    tasks_done = Tasks.objects.filter(status='DONE')
    tasks_canceled = Tasks.objects.filter(status='CANCELED')
    tasks_expired = Tasks.objects.filter(status='EXPIRED')

    context = {
        'users': users,
        'tasks': tasks,
        'departments': departments,
        'tasks_status': [
            tasks_new.count(),
            tasks_in_progress.count(),
            tasks_done.count(),
            tasks_canceled.count(),
            tasks_expired.count()
        ],
    }
    return render(request, 'KPIapp/Supervisor/supervisor.html', context)


@login_required(login_url='signIn')
def view_department(request):
    sort_by = request.GET.get('sort_by', 'id')
    search_by = request.GET.get('search_by')

    departments = Departments.objects.all().order_by(sort_by)

    if search_by:
        departments = Departments.objects.filter(name__icontains=search_by).order_by(sort_by)

    context = {
        'departments': departments,
    }
    return render(request, 'KPIapp/Supervisor/view_department.html', context)


@login_required(login_url='signIn')
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_department')
    form = DepartmentForm
    context = {'form': form}
    return render(request, 'KPIapp/Supervisor/add_department.html', context)


@login_required(login_url='signIn')
def edit_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('view_department')
    form = DepartmentForm(instance=department)
    context = {'form': form}
    return render(request, 'KPIapp/Supervisor/add_department.html', context)


@login_required(login_url='signIn')
def delete_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    department.delete()
    return redirect('view_department')


@login_required(login_url='signIn')
def view_employee(request):
    sort_by = request.GET.get('sort_by', 'id')
    search_by = request.GET.get('search_by')

    users = User.objects.all().order_by(sort_by)

    if search_by:
        users = User.objects.filter(username__icontains=search_by).order_by(sort_by)

    context = {
        'users': users,
    }
    return render(request, 'KPIapp/Supervisor/view_employee.html', context)


@login_required(login_url='signIn')
def add_employee(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            department = form.cleaned_data.get('department')
            user.save()
            if department:
                department.users.add(user)
            form.save()
            return redirect('view_employee')
    form = UserForm
    context = {'form': form}
    return render(request, 'KPIapp/Supervisor/add_employee.html', context)


@login_required(login_url='signIn')
def edit_employee(request, employee_id):
    user = User.objects.get(id=employee_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            users = form.save(commit=False)
            department = form.cleaned_data.get('department')
            users.save()
            if department:
                department.users.add(users)
            form.save()
            return redirect('view_employee')
        else:
            print(form.errors)
    form = UserEditForm(instance=user)
    context = {'form': form}
    return render(request, 'KPIapp/Supervisor/add_employee.html', context)


def delete_employee(request, employee_id):
    user = User.objects.get(id=employee_id)
    user.delete()
    return redirect('view_employee')


def view_tasks(request, filter_by=None):
    tasks_low = Tasks.objects.filter(priority='LOW')
    tasks_medium = Tasks.objects.filter(priority='MEDIUM')
    tasks_high = Tasks.objects.filter(priority='HIGH')
    tasks_critical = Tasks.objects.filter(priority='CRITICAL')

    tasks_new = Tasks.objects.filter(status='NEW')
    tasks_in_progress = Tasks.objects.filter(status='IN_PROGRESS')
    tasks_done = Tasks.objects.filter(status='DONE')
    tasks_canceled = Tasks.objects.filter(status='CANCELED')
    tasks_expired = Tasks.objects.filter(status='EXPIRED')

    departments = Departments.objects.all()

    users = User.objects.all()

    if filter_by == 'priority':
        template = 'KPIapp/includes/tasks/priority-tasks.html'
    elif filter_by == 'department':
        template = 'KPIapp/includes/tasks/department-card.html'
    elif filter_by == 'staff':
        template = 'KPIapp/includes/tasks/staff-tasks.html'
    elif filter_by == 'status':
        template = 'KPIapp/includes/tasks/status-tasks.html'
    else:
        template = 'KPIapp/includes/tasks/all-tasks.html'

    tasks = Tasks.objects.all()

    for task in tasks:
        if str(task.deadline) < datetime.now().strftime("%Y-%m-%d %H:%M:%S") and task.status != 'DONE':
            task.status = 'EXPIRED'
            task.save()
        if task.mark != "0" and task.ended_at is None:
            task.ended_at = datetime.now()
            task.status = 'DONE'
            task.save()

    context = {
        'tasks': tasks,
        'include_template': template,
        'tasks_priority': {
            'tasks_low': tasks_low,
            'tasks_medium': tasks_medium,
            'tasks_high': tasks_high,
            'tasks_critical': tasks_critical
        },
        'tasks_status': {
            'tasks_new': tasks_new,
            'tasks_in_progress': tasks_in_progress,
            'tasks_done': tasks_done,
            'tasks_canceled': tasks_canceled,
            'tasks_expired': tasks_expired
        },
        'departments': departments,
        'users': users

    }
    return render(request, 'KPIapp/view_tasks.html', context)


def add_tasks(request):
    users = User.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('user')
            title = form.cleaned_data.get('title')
            task_id = form.cleaned_data.get('id')
            email = user.email
            sms = f'Hello {user.username}!\n You have a new task!\n Title: {title}\n'
            for_email = sms + "Click here to see it: http://127.0.0.1:8000/view_tasks"

            message = EmailMessage('New Task', for_email, to=[email])
            message.send()

            notifications = Notifications.objects.create(
                user=user,
                text=sms,
                task_id=task_id
            )
            notifications.save()
            return redirect('view_tasks')

    form = TaskForm()
    context = {
        'users': users,
        'form': form
    }
    return render(request, 'KPIapp/add_tasks.html', context)


def edit_tasks(request, task_id):
    users = User.objects.all()
    task = Tasks.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('view_tasks')
        else:
            print(form.errors)
    form = TaskForm(instance=task)
    context = {
        'users': users,
        'form': form
    }
    return render(request, 'KPIapp/add_tasks.html', context)


def edit_tasks_employee(request, task_id):
    task = Tasks.objects.get(id=task_id)
    notifications = Notifications.objects.filter(task_id=task_id)
    if notifications:
        notifications.status = True
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('view_tasks')
    form = EditTaskForm(instance=task)
    context = {
        'form': form
    }
    return render(request, 'KPIapp/Employee/edit-task-employee.html', context)


def delete_tasks(request, task_id):
    task = Tasks.objects.get(id=task_id)
    task.delete()
    return redirect('view_tasks')