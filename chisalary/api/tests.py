from django.test import TestCase
from rest_framework.test import APIClient
from .manager import EmployeeManager
from .models import Employee


test_employees = [{
        "id": 1,
        "first_name": "KEVIN",
        "middle_name": "D",
        "last_name": "BRUNO",
        "job_titles": "SERGEANT",
        "department": "POLICE",
        "full_or_part_time": "F",
        "salary_or_hourly": "Salary",
        "typical_hours": None,
        "annual_salary": "104628",
        "hourly_rate": None
    },
    {
        "id": 2,
        "first_name": "JOHN",
        "middle_name": "E",
        "last_name": "COOPER",
        "job_titles": "LIEUTENANT-EMT",
        "department": "FIRE",
        "full_or_part_time": "F",
        "salary_or_hourly": "Salary",
        "typical_hours": None,
        "annual_salary": "114324",
        "hourly_rate": None
    }
]


class EmployeeTaskTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.employee_1 = Employee.objects.create(**test_employees[0])
        self.employee_2 = Employee.objects.create(**test_employees[1])
        self.employees = [self.employee_1, self.employee_2]

    def test_employee_field_changes(self):

        current_salary = '104628'
        new_salary = '123456'

        self.assertEqual(self.employee_1.annual_salary, current_salary)

        # change employee salary
        updated_test_employees = test_employees
        updated_test_employees[0]['annual_salary'] = new_salary

        EmployeeManager().sync_db(updated_test_employees)

        # check that salary has been updated correctly
        updated_employee_1 = Employee.objects.get(id=self.employee_1.id)
        self.assertEqual(updated_employee_1.annual_salary, new_salary)

    def test_clean_employee_name(self):
        employee = {'name': 'BRUNO,  KEVIN D'}
        expected_employee = {'first_name': 'KEVIN', 'last_name': 'BRUNO', 'middle_name': 'D'}

        cleaned_employee = EmployeeManager().clean(employee)
        self.assertEqual(cleaned_employee, expected_employee)
