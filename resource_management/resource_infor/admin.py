from django.contrib import admin
from .models import Company, Employees

admin.sites.site.register(Company)
admin.sites.site.register(Employees)
