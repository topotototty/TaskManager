from TaskManagerApp.models import Employee

def employee_context_processor(request):
    if request.user.is_authenticated:
        try:
            employee = Employee.objects.get(user=request.user)
            return {'employee': employee}
        except Employee.DoesNotExist:
            return {}
    return {}