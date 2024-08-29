from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from KPIapp.models import User, Tasks, TasksAnswers, Departments, Role, Notifications

# Register your models here.
admin.site.register([User, Tasks, TasksAnswers, Departments, Role, Notifications])