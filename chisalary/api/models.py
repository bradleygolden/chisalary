from django.db import models
from nameparser import HumanName


class Employee(models.Model):
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    job_titles = models.CharField(max_length=128)
    department = models.CharField(max_length=64)
    full_or_part_time = models.CharField(max_length=16)
    salary_or_hourly = models.CharField(max_length=16)
    typical_hours = models.IntegerField(null=True)
    annual_salary = models.IntegerField(null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def full_name(self):
        name = '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)
        return str(HumanName(name))

    def __str__(self):
        return self.full_name()