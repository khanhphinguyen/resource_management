from django.urls import path, re_path
from . import views

app_name = 'resource_infor'
urlpatterns = [
    path('', views.CompanyReturnList.as_view(), name='company'),
    path('company/json/', views.CompanyView.as_view(), name='company_json'),
    path('employees/', views.EmployeesReturnList.as_view(max_return=3), name='employee_list'),
    path('<int:company_pk>/employees/', views.employees_detail, name='employees_detail'),
    re_path(r'^employees/json/', views.EmployeesView.as_view(), name='employees_json'),
    path('listview/', views.EmployeesList.as_view()),
    path('detailview/<int:pk>', views.CompanyDetailView.as_view()),
    path('employee/<company>/', views.CompanyEmployeeList.as_view(), name='employees_by_company'),
]