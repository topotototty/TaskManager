from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Tasks, TaskStatus

@receiver(pre_save, sender=Tasks)
def update_task_status(sender, instance, **kwargs):
    if instance.status.title != "Выполнена":
        if instance.deadline < timezone.now().date():
            overdue_status = TaskStatus.objects.get(title="Просрочена")
            instance.status = overdue_status
