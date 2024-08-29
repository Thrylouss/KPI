from django.urls import path

from KPIapp import views

urlpatterns = [
    path('employee/', views.employee, name='employee'),
    path('', views.supervisor, name='supervisor'),
    path('view_employee/', views.view_employee, name='view_employee'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name='delete_employee'),
    path('view_tasks/', views.view_tasks, name='view_tasks'),
    path('view_tasks/priority/', views.view_tasks, {'filter_by': 'priority'}, name='priority_tasks'),
    path('view_tasks/department/', views.view_tasks, {'filter_by': 'department'}, name='department_tasks'),
    path('view_tasks/staff/', views.view_tasks, {'filter_by': 'staff'}, name='staff_tasks'),
    path('view_tasks/status/', views.view_tasks, {'filter_by': 'status'}, name='status_tasks'),
    path('add_tasks/', views.add_tasks, name='add_tasks'),
    path('edit_tasks/<int:task_id>/', views.edit_tasks, name='edit_tasks'),
    path('delete_tasks/<int:task_id>/', views.delete_tasks, name='delete_tasks'),
    path('view_department/', views.view_department, name='view_department'),
    path('add_department/', views.add_department, name='add_department'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('edit_tasks/employee/<int:task_id>/', views.edit_tasks_employee, name='edit_tasks_employee'),
]
