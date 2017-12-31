from decimal import Decimal
from django.test import TestCase
from django.utils.http import urlencode
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .manager import EmployeeManager, EmployeesManager
from .models import Employee


dirty_test_employees = [
    {
        "annual_salary": "104628",
        "department": "POLICE",
        "full_or_part_time": "F",
        "job_titles": "SERGEANT",
        "name": "BRUNO,  KEVIN D",
        "salary_or_hourly": "Salary"
    },
    {
        "department": "OEMC",
        "full_or_part_time": "P",
        "hourly_rate": "19.86",
        "job_titles": "TRAFFIC CONTROL AIDE-HOURLY",
        "name": "WALLACE,  DEBRA ",
        "salary_or_hourly": "Hourly",
        "typical_hours": "20"
    },
]

clean_test_employees = [
        {
            "first_name": "AZIZ",
            "middle_name": "",
            "last_name": "ABDELMAJEID",
            "job_titles": "POLICE OFFICER",
            "department": "POLICE",
            "full_or_part_time": "F",
            "salary_or_hourly": "Salary",
            "typical_hours": None,
            "annual_salary": int("84054"),
            "hourly_rate": None
        },
        {
            "first_name": "DEBRA",
            "last_name": "WALLACE",
            "department": "OEMC",
            "full_or_part_time": "P",
            "hourly_rate": Decimal("19.86"),
            "job_titles": "TRAFFIC CONTROL AIDE-HOURLY",
            "salary_or_hourly": "Hourly",
            "typical_hours": 20
        },
    ]


class EmployeeManagerTestCase(TestCase):

    def test_clean_employee_name(self):
        expected_first_name = 'KEVIN'
        expected_last_name = 'BRUNO'
        expected_middle_name = 'D'

        employee_manager = EmployeeManager(dirty_test_employees[0])
        employee = employee_manager.clean_name().employee

        self.assertEqual(employee['first_name'], expected_first_name)
        self.assertEqual(employee['middle_name'], expected_middle_name)
        self.assertEqual(employee['last_name'], expected_last_name)

    def test_clean_full_time_employee_annual_salary(self):
        expected_annual_salary = '104628'

        employee_manager = EmployeeManager(dirty_test_employees[0])
        employee = employee_manager.clean_annual_salary().employee

        self.assertEqual(employee['annual_salary'], expected_annual_salary)

    def test_clean_part_time_employee_annual_salary(self):
        employee_manager = EmployeeManager(dirty_test_employees[1])
        employee = employee_manager.clean_annual_salary().employee

        with self.assertRaises(KeyError):
            employee['annual_salary']

    def test_clean_part_time_employee_hourly_rate(self):

        expected_hourly_rate = '19.86'

        employee_manager = EmployeeManager(dirty_test_employees[1])
        employee = employee_manager.clean_hourly_rate().employee

        self.assertEqual(employee['hourly_rate'], expected_hourly_rate)

    def test_clean_full_time_employee_hourly_rate(self):
        employee_manager = EmployeeManager(dirty_test_employees[0])
        employee = employee_manager.clean_annual_salary().employee

        with self.assertRaises(KeyError):
            employee['hourly_rate']


class EmployeesManagerTestCase(TestCase):

    def test_sync_employees_with_prepopulated_employees(self):
        employees_manager = EmployeesManager()
        employees_manager.sync_employees(employees=clean_test_employees, progress_bar=False)

        employees = Employee.objects.all()

        self.assertEqual(len(employees), 2)

        for i, employee in enumerate(employees):
            self.assertEqual(employee.first_name, clean_test_employees[i]['first_name'])
            if 'middle_name' in clean_test_employees[i]:
                self.assertEqual(employee.middle_name, clean_test_employees[i]['middle_name'])
            self.assertEqual(employee.last_name, clean_test_employees[i]['last_name'])
            self.assertEqual(employee.job_titles, clean_test_employees[i]['job_titles'])
            self.assertEqual(employee.department, clean_test_employees[i]['department'])
            self.assertEqual(employee.full_or_part_time, clean_test_employees[i]['full_or_part_time'])
            self.assertEqual(employee.salary_or_hourly, clean_test_employees[i]['salary_or_hourly'])
            self.assertEqual(employee.typical_hours, clean_test_employees[i]['typical_hours'])
            if 'annual_salary' in clean_test_employees[i]:
                self.assertEqual(employee.annual_salary, clean_test_employees[i]['annual_salary'])
            if 'hourly_rate' in clean_test_employees[i]:
                self.assertEqual(employee.hourly_rate, clean_test_employees[i]['hourly_rate'])


class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        self.create_employees()

    def create_employees(self):
        employees_manager = EmployeesManager()
        employees_manager.sync_employees(employees=clean_test_employees, progress_bar=False)

    def test_retrieve_employees_list(self):
        url = reverse('employee-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['results'][0]['first_name'], 'AZIZ')
        self.assertEqual(response.data['results'][1]['first_name'], 'DEBRA')

    def test_retrieve_employee_detail(self):
        employee_id = 1
        url = reverse('employee-detail', args=[employee_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'AZIZ')

    def test_search_employees_by_first_name(self):
        base_url = reverse('employee-list')
        search_by_first_name = urlencode({'search': 'DEB', 'filter': 'first_name'})
        url = f'{base_url}?{search_by_first_name}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'DEBRA')

    def test_filter_employees_by_min_annual_salary(self):
        base_url = reverse('employee-list')
        search_by_min_annual_salary = urlencode({'min_annual_salary': 84054})
        url = f'{base_url}?{search_by_min_annual_salary}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'AZIZ')

        # no employee with minimum of 1,000,000 salary
        search_by_min_annual_salary = urlencode({'min_annual_salary': 1000000})
        url = f'{base_url}?{search_by_min_annual_salary}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_filter_employees_by_max_annual_salary(self):
        base_url = reverse('employee-list')
        search_by_max_annual_salary = urlencode({'max_annual_salary': 84054})
        url = f'{base_url}?{search_by_max_annual_salary}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'AZIZ')

        # no employee with maximum of 1 salary
        search_by_min_annual_salary = urlencode({'max_annual_salary': 1})
        url = f'{base_url}?{search_by_min_annual_salary}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_filter_employees_by_min_hourly_rate(self):
        base_url = reverse('employee-list')
        search_by_min_hourly_rate = urlencode({'min_hourly_rate': 19.86})
        url = f'{base_url}?{search_by_min_hourly_rate}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'DEBRA')

        # no employee with minimum of 1,000,000 rate
        search_by_min_hourly_rate = urlencode({'min_hourly_rate': 1000000})
        url = f'{base_url}?{search_by_min_hourly_rate}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_filter_employees_by_max_hourly_rate(self):
        base_url = reverse('employee-list')
        search_by_max_hourly_rate = urlencode({'max_hourly_rate': 19.86})
        url = f'{base_url}?{search_by_max_hourly_rate}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'DEBRA')

        # no employee with max of 1 rate
        search_by_max_hourly_rate = urlencode({'max_hourly_rate': 1})
        url = f'{base_url}?{search_by_max_hourly_rate}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)


class EmployeeModelTestCase(TestCase):

    def test_string_representation(self):
        employee = Employee(**clean_test_employees[0])
        self.assertEqual(str(employee), 'AZIZ ABDELMAJEID')
