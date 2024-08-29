from django.urls import path

from UserApp import views

urlpatterns = [
    path('signIn/', views.sign_in, name='signIn'),
    path('logOut/', views.log_out, name='logOut'),
]