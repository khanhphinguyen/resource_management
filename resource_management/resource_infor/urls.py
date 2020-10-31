from django.urls import path
from .views import company, employees
from . import views

urlpatterns = [
    path('company', company, name='company_list'),
    path('employees', employees, name='employees_list'),
    path('company_json', views.CompanyView.as_view(), name='company_list_json'),
    path('employees_json', views.EmployeesView.as_view(), name='employees_list_json'),
]