from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .forms import LoginForm


# Create your views here.
def sign_in(request):
    if request.user.is_authenticated:
        if request.user.role.name == 'employee':
            return redirect('employee')
        if request.user.role.name == 'Supervisor':
            return redirect('supervisor')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('signIn')
            login(request, user)
            if request.user.role.name == 'employee':
                return redirect('employee')
            if request.user.role.name == 'Supervisor':
                return redirect('supervisor')

    form = LoginForm()
    context = {'form': form}
    return render(request, 'UserApp/login.html', context)


def log_out(request):
    logout(request)
    return redirect('signIn')