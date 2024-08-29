import math

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Role (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(on_delete=models.CASCADE, related_name='role', to=Role, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default_avatar.jpg')
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    choices = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
    ]
    gender = models.CharField(choices=choices, default="MALE", max_length=100)

    def __str__(self):
        return self.username

    def get_departament(self):
        departments = Departments.objects.filter(users=self)
        return departments.first() if departments.exists() else None

    def get_tasks(self):
        tasks = Tasks.objects.filter(user=self)
        return tasks if tasks.exists() else None

    def get_employment(self):
        tasks = Tasks.objects.count()
        user_tasks = Tasks.objects.filter(user=self).count()
        if user_tasks == 0:
            return 0
        return math.floor((user_tasks / tasks) * 100)

    def get_notification(self):
        notifications = Notifications.objects.filter(user=self)
        return notifications


class Departments(models.Model):
    name = models.CharField(max_length=100)
    responsible = models.ForeignKey(on_delete=models.CASCADE, related_name='users', to=User, null=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_tasks(self):
        tasks = Tasks.objects.filter(department=self)
        return tasks if tasks.exists() else None


class Tasks(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    choices_employee = [
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
        ("CANCELED", "Canceled")
    ]
    choices = [
        ("NEW", "New"),
        ("IN_PROGRESS", "In Progress"),
        ("DONE", "Done"),
        ("CANCELED", "Canceled"),
        ("EXPIRED", "Expired"),
    ]
    status = models.CharField(choices=choices, default="NEW", max_length=100)
    choices_mark = [
        ("0", "0"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    ]
    mark = models.CharField(choices=choices_mark, default="0", max_length=100)
    choices_priority = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("CRITICAL", "Critical"),
    ]
    priority = models.CharField(choices=choices_priority, default="LOW", max_length=100)
    ended_at = models.DateTimeField(null=True, blank=True)
    department = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='department',
        to=Departments,
        default='Departments')
    boss = models.ForeignKey(on_delete=models.CASCADE, related_name='boss', to=User, default="Appointed")
    user = models.ForeignKey(on_delete=models.CASCADE, related_name='user', to=User)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_tasks, created = TotalTasks.objects.get_or_create(user=self.user)
        total_tasks.total_tasks = Tasks.objects.filter(user=self.user).count()
        total_tasks.save()

    def __str__(self):
        return self.title


class TasksAnswers(models.Model):
    task = models.ForeignKey(on_delete=models.CASCADE, related_name='task', to=Tasks)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True, blank=True)
    answer = models.CharField(max_length=250)
    user = models.ForeignKey(on_delete=models.CASCADE, related_name='user_answer', to=User)
    author = models.ForeignKey(on_delete=models.CASCADE, related_name='author', to=User)

    def __stt__(self):
        return self.task


class Notifications(models.Model):
    text = models.CharField(max_length=255)
    task_id = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(on_delete=models.CASCADE, related_name='user_notif', to=User)
    status = models.BooleanField(default=False, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.text


class TotalTasks(models.Model):
    total_tasks = models.IntegerField(default=0)
    user = models.ForeignKey(on_delete=models.CASCADE, related_name='user_total', to=User)

    def __str__(self):
        return self.user
