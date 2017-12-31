from rest_framework import viewsets
from .models import Employee
from .filters import EmployeeFilter
from .serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    filter_class = EmployeeFilter
    search_fields = (
        '^first_name',
        '^middle_name',
        '^last_name',
        '^job_titles',
        '^department',
        '^annual_salary',
        '^hourly_rate',
        )
    ordering_fields = (
        'first_name',
        'middle_name',
        'last_name',
        'job_titles',
        'department',
        'annual_salary',
        'hourly_rate',
        )
