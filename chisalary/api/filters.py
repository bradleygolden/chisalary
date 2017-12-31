from django_filters import FilterSet, NumberFilter
from .models import Employee


class EmployeeFilter(FilterSet):
    min_annual_salary = NumberFilter(
        name='annual_salary', lookup_expr='gte')
    max_annual_salary = NumberFilter(
        name='annual_salary', lookup_expr='lte')

    class Meta:
        model = Employee
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'job_titles',
            'department',
            'hourly_rate',
            'annual_salary',
            'min_annual_salary',
            'max_annual_salary',
            )
