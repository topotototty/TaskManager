from django.contrib import admin
from django.urls import path, include
from TaskManagerApp.views import *
from TaskManagerApp.models import *
import TaskManagerApp.views as v

positions_patterns = [
    path('', v.position_list, name='position_list'),
    path('add/', AddPositionView.as_view(), name='add_position'),
    path('edit/<int:pk>/', EditPositionView.as_view(), name='edit_position'),
    path('delete/<int:pk>/', v.delete_position, name='delete_position'),
]

employees_patterns = [
    path('', v.employees_list, name='employees_list'),
    path('add/', AddEmployeeView.as_view(), name='add_employee'),
    path('edit/<int:employee_id>/', EditEmployeeView.as_view(), name='edit_employee'),
    path('delete/<int:employee_id>/', v.delete_employee, name='delete_employee'),
]

tasks_patterns = [
    path('', v.tasks_list, name='tasks_list'),
    path('accept/<int:task_id>/', v.accept_task, name='accept_task'),
    path('complete/<int:task_id>/', complete_task, name='complete_task'),
    path('add/', AddTaskView.as_view(), name='add_task'),
    path('delete/<int:task_id>/', DeleteTaskView.as_view(), name='delete_task'),
    path('edit/<int:task_id>/', EditTaskView.as_view(), name='edit_task'),
]

urlpatterns = [
    path('', v.login_view, name='login'),
    path('admin/', admin.site.urls),
    path('profile/', v.profile_view, name='profile'),
    path('logout/', v.logout_view, name='logout'),
    path('positions/', include(positions_patterns)),
    path('employees/', include(employees_patterns)),
    path('tasks/', include(tasks_patterns)),
]

