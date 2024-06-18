from django.contrib.auth.models import User
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Position(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Наименование")
    salary = models.FloatField(verbose_name="Зарплата")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    first_name = models.CharField(max_length=50, verbose_name="Имя сотрудника")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия сотрудника")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество сотрудника")
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name="Номер телефона сотрудника")
    email = models.EmailField(blank=True, null=True, verbose_name="Электронная почта сотрудника")
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

class TaskStatus(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Наименование")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"


class Tasks(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    deadline = models.DateField(verbose_name="Срок сдачи")
    assignee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Исполнитель")
    assigner = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="assigned_tasks", verbose_name="Назначил", blank=True, null=True)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, verbose_name="Статус")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
