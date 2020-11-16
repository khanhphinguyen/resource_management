from django.urls import path, re_path
from . import views

app_name = 'resource_infor'
urlpatterns = [
    path('', views.company, name='company'),
    path('<int:company_pk>/employees/', views.employees_detail, name='employees_detail'),
    path('company/json/', views.CompanyView.as_view(), name='company_json'),
    re_path(r'^employees/json/', views.EmployeesView.as_view(), name='employees_json'),
]