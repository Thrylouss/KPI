from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Tasks, TasksAnswers, Role, Departments, Notifications


class UserForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    department = forms.ModelChoiceField(
        queryset=Departments.objects.all(),
        required=False,
        empty_label="Select Department")
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Select Role",
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'role', 'department', 'phone', 'email', 'gender')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }


class UserEditForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        empty_label="Select Role",
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'role', 'phone', 'email', 'gender', 'about')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'about': forms.Textarea(attrs={'placeholder': 'Write here something about you'}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('title', 'description', 'priority', 'status', 'deadline', 'boss', 'department', 'user', 'mark')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "Title"}),
            'description': forms.TextInput(attrs={'placeholder': "Description"}),
            'deadline': forms.DateTimeInput(attrs={'placeholder': "YYYY-MM-DD HH:MM:SS", 'type': 'datetime-local'}),
        }


class EditTaskForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Tasks.choices_employee)

    class Meta:
        model = Tasks
        fields = ('title', 'description', 'deadline', 'priority', 'status')
        widgets = {
            "title": forms.TextInput(attrs={'placeholder': "Title", 'readonly': True}),
            "description": forms.TextInput(attrs={'placeholder': "Description", 'readonly': True}),
            "deadline": forms.TextInput(attrs={'placeholder': "YYYY-MM-DD HH:MM:SS", 'type': 'datetime-local', 'readonly': True}),
            "priority": forms.TextInput(attrs={'placeholder': "Priority", 'readonly': True}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ('name', 'responsible', 'users')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': "Name"}),
            'responsible': forms.Select(attrs={'placeholder': "Responsible"}),
            'users': forms.SelectMultiple(attrs={'placeholder': "Employees"}),
        }