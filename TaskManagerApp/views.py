import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from .models import Employee, Position, TaskStatus, Tasks

def get_employee(request):
    return get_object_or_404(Employee, user=request.user)


def get_task_status(title):
    return get_object_or_404(TaskStatus, title=title)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль.')
    return render(request, 'Auth/login.html')


@login_required(login_url=reverse_lazy('login'))
def profile_view(request):
    employee = get_employee(request)
    statuses = {
        "assigned": get_task_status("Назначена"),
        "in_progress": get_task_status("Взята в работу"),
        "completed": get_task_status("Выполнена"),
    }

    employees = Employee.objects.exclude(position__title="Администратор")
    tasks_assigned_by_user = Tasks.objects.filter(assigner=employee, status__in=[statuses["assigned"], statuses["in_progress"]])
    tasks_assigned_to_user = Tasks.objects.filter(assignee=employee, status=statuses["in_progress"])
    completed_tasks_by_user = Tasks.objects.filter(assignee=employee, status=statuses["completed"])

    return render(request, 'Profile/profile.html', {
        'employee': employee,
        'tasks': tasks_assigned_by_user,
        'my_tasks': tasks_assigned_to_user,
        'my_completed_tasks': completed_tasks_by_user,
        'employees': employees
    })


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('login'))


@login_required(login_url=reverse_lazy('login'))
def position_list(request):
    positions = Position.objects.all()
    return render(request, 'Positions/positions.html', {'positions': positions})


class AddPositionView(View):
    def post(self, request):
        Position.objects.create(
            title=request.POST.get('title'),
            salary=request.POST.get('salary')
        )
        return redirect('position_list')


class EditPositionView(View):
    def post(self, request, pk):
        position = get_object_or_404(Position, pk=pk)
        position.title = request.POST.get('title')
        position.salary = request.POST.get('salary')
        position.save()
        return redirect('position_list')


def delete_position(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == 'POST':
        if position.title == "Администратор":
            messages.error(request, "Нельзя удалить должность 'Администратор'.")
        else:
            position.delete()
            messages.success(request, "Должность успешно удалена.")
    return redirect('position_list')


@login_required(login_url=reverse_lazy('login'))
def employees_list(request):
    employees = Employee.objects.all()
    positions = Position.objects.all()
    sorted_employees = employees

    if request.method == 'POST':
        if 'sort_asc' in request.POST:
            sorted_employees = employees.order_by('last_name', 'first_name')
        elif 'sort_desc' in request.POST:
            sorted_employees = employees.order_by('-last_name', '-first_name')

    return render(request, 'Employees/employees.html', {
        'employees': sorted_employees,
        'positions': positions
    })


class AddEmployeeView(View):
    def post(self, request):
        user = User.objects.create(
            username=request.POST.get('username'),
            password=make_password(request.POST.get('password')),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email')
        )

        Employee.objects.create(
            user=user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            middle_name=request.POST.get('middle_name'),
            phone_number=request.POST.get('phone_number'),
            email=request.POST.get('email'),
            position=get_object_or_404(Position, title=request.POST.get('position'))
        )
        return redirect('employees_list')


class EditEmployeeView(View):
    def post(self, request, employee_id):
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.middle_name = request.POST.get('middle_name')
        employee.phone_number = request.POST.get('phone_number')
        employee.email = request.POST.get('email')
        employee.position = get_object_or_404(Position, title=request.POST.get('position'))
        employee.save()
        return redirect('employees_list')


def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        if employee.position.title == "Администратор":
            messages.error(request, "Нельзя удалить администратора.")
        else:
            employee.user.delete()
            employee.delete()
            messages.success(request, "Сотрудник успешно удален.")
    return redirect('employees_list')


@login_required(login_url=reverse_lazy('login'))
def tasks_list(request):
    employee = get_employee(request)

    statuses = {
        "assigned": get_task_status("Назначена"),
        "in_progress": get_task_status("Взята в работу"),
        "completed": get_task_status("Выполнена"),
        "overdue": get_task_status("Просрочена"),
    }

    employees = Employee.objects.exclude(position__title="Администратор")
    statuses_list = TaskStatus.objects.all()

    if employee.position.title in ['Администратор', 'Менеджер']:
        tasks = Tasks.objects.filter(status__in=[statuses["assigned"], statuses["in_progress"]])
        completed_tasks = Tasks.objects.filter(status=statuses["completed"])
        overdue_tasks = Tasks.objects.filter(status=statuses["overdue"])
    else:
        tasks = Tasks.objects.filter(status=statuses["assigned"])
        completed_tasks = Tasks.objects.filter(assigner=employee, status=statuses["completed"])
        overdue_tasks = Tasks.objects.filter(assigner=employee, status=statuses["overdue"])

    return render(request, 'Tasks/tasks.html', {
        'employee': employee,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'employees': employees,
        'statuses': statuses_list
    })


@login_required(login_url=reverse_lazy('login'))
def accept_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    in_progress_status = get_task_status("Взята в работу")
    employee = get_employee(request)

    if task.assigner == employee:
        messages.error(request, "Вы не можете принять свою задачу")
    else:
        task.status = in_progress_status
        task.assignee = employee
        task.save()
        messages.success(request, "Задача успешно принята, загляните в личный кабинет")

    return redirect('tasks_list')


@login_required(login_url=reverse_lazy('login'))
def complete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    completed_status = get_task_status("Выполнена")

    task.status = completed_status
    task.save()
    messages.success(request, "Задача успешно завершена")
    return redirect('profile')


@method_decorator(login_required, name='dispatch')
class AddTaskView(View):
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline_str = request.POST.get('deadline')
        assignee_id = request.POST.get('assignee')
        assignee = get_object_or_404(Employee, pk=assignee_id) if assignee_id else None
        assigner = get_employee(request)

        if assignee and assignee.position.title == 'Администратор':
            messages.error(request, "Администратора нельзя назначить исполнителем")
        elif assignee == assigner:
            messages.error(request, "Вы не можете назначить себя исполнителем")
        else:
            assigned_status = get_task_status("Назначена")
            in_progress_status = get_task_status("Взята в работу")

            try:
                deadline = datetime.datetime.strptime(deadline_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Неверный формат даты")
                return redirect('tasks_list')

            Tasks.objects.create(
                title=title,
                description=description,
                deadline=deadline,
                assignee=assignee,
                assigner=assigner,
                status=in_progress_status if assignee else assigned_status
            )
            messages.success(request, "Задача успешно назначена")

        return redirect('tasks_list')


@method_decorator(login_required, name='dispatch')
class DeleteTaskView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Tasks, pk=task_id)
        employee = get_employee(request)

        if employee.position.title == 'Администратор' or task.assigner == employee:
            task.delete()
            messages.success(request, "Задача успешно удалена")
        else:
            messages.error(request, "Вы не можете удалить эту задачу")

        return redirect('tasks_list')


@method_decorator(login_required, name='dispatch')
class EditTaskView(View):
    def post(self, request, task_id):
        task = get_object_or_404(Tasks, pk=task_id)
        employee = get_employee(request)

        if employee.position.title != 'Администратор' and task.assigner != employee:
            messages.error(request, "У вас нет прав для изменения этой задачи.")
        else:
            title = request.POST.get('title')
            description = request.POST.get('description')
            deadline_str = request.POST.get('deadline')
            assignee_id = request.POST.get('assignee')
            assignee = get_object_or_404(Employee, pk=assignee_id) if assignee_id else None

            try:
                deadline_date = datetime.datetime.strptime(deadline_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Неправильный формат даты.")
                return redirect('tasks_list')

            task.title = title
            task.description = description
            task.deadline = deadline_date
            task.assignee = assignee
            task.save()

            messages.success(request, "Задача успешно изменена")

        return redirect('tasks_list')