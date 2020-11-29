from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, DetailView

from .models import Company, Employees

from rest_framework import views
from rest_framework.response import Response

# Practice View, decorating
decorator = [never_cache, login_required]
@method_decorator(decorator, name='get')
class CompanyReturnList(View):
    model_class = Company
    template_name = 'resource_infor/company.html'
    variable_name = 'companies'
    variable_count = 'employees'
    max_return = 5

    def get(self, request, *args, **kwargs):
        content_ob = self.model_class.objects.annotate(count_num=Count(self.variable_count)).order_by('-count_num')[:self.max_return]
        return render(request, self.template_name, {self.variable_name: content_ob})

# Practice mixins-inherited
class EmployeesReturnList(CompanyReturnList):
    model_class = Employees
    template_name = 'resource_infor/detail.html'
    variable_name = 'content_ob'
    variable_count = 'employee_age'

# Practice ListView
class EmployeesList(ListView):
    model = Employees
    context_object_name = 'all_employee_list'

class CompanyDetailView(DetailView):
    context_object_name = 'all_company_list'
    queryset = Company.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee_list'] = Employees.objects.all()
        return context

class CompanyEmployeeList(ListView):
    template_name = 'resource_infor/employees_list.html'

    def get_queryset(self):
        self.company = get_object_or_404(Company, company_name=self.kwargs['company'])
        return Employees.objects.filter(company=self.company)

# Practice function-base view
def employees_detail(request, company_pk):
    employees_list = Employees.objects.filter(company_id=company_pk)
    context = {'employees': employees_list}
    response = render(request, 'resource_infor/employees.html', context)
    return response

# Practice rest-framework
class CompanyView(views.APIView):
    '''
    API endpoint that allows company list to be views or edit.
    '''
    def get(self, request, format=None):
        '''
        :return: all company list in JSON group by location
        '''
        company_list_return = []

        # get and sort location list
        location = Company.objects.values_list('company_location', flat=True)
        location_set = set(location)
        location_list = list(location_set)
        location_list.sort()

        for location in location_list:
            company_query = Company.objects.filter(company_location=location).annotate(TotalEmployees=Count('employees')).order_by('-TotalEmployees','company_name').values('company_name','company_location','TotalEmployees')
            company_list = list(company_query)
            company_list_return.extend(company_list)
        return Response(company_list_return)

class EmployeesView(views.APIView):
    def get(self, request, format=None):
        '''
        API return all employees group by level
        :return: JSON
        '''

        level_set = set(Employees.objects.values_list('level', flat=True))
        level_list = list(level_set)
        level_list.sort()

        employeesreturn = []
        for level in level_list:
            employees_list = list(Employees.objects.filter(level=level).order_by('join_date','employee_name').values())
            employeesreturn.extend(employees_list)
        return Response(employeesreturn)

