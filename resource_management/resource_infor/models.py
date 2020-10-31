from django.db import models

# Company class model
class Company(models.Model):
    company_name = models.CharField(max_length=200, unique=True)
    company_location = models.CharField(max_length=100, default='Ho Chi Minh')

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name

# Employees class model
class Employees(models.Model):
    employee_name = models.CharField(max_length=50, blank=False)
    employee_age  = models.IntegerField(default=18)
    join_date = models.DateField('Date Published')
    company = models.ForeignKey(Company, on_delete = models.CASCADE)
    level_choice = [
        ('BE','Beginner'),
        ('JU','Junior'),
        ('SE','Senior'),
        ('EX','Expect'),
        ('MA','Master'),
        ('GU','Guru'),
    ]
    level = models.CharField(max_length=2,choices=level_choice, default='BE')

    def __str__(self):
        return self.employee_name