from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    job_titles = models.CharField(max_length=128)
    department = models.CharField(max_length=64)
    full_or_part_time = models.CharField(max_length=16)
    salary_or_hourly = models.CharField(max_length=16)
    typical_hours = models.IntegerField(null=True)
    annual_salary = models.CharField(max_length=32, null=True)
    hourly_rate = models.CharField(max_length=32, null=True)
