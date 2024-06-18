from django.contrib import admin
from .models import *

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'position')
    
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'salary')

@admin.register(TaskStatus)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', )

@admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'deadline', 'status')