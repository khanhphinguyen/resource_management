from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from .models import Company, Employees
from rest_framework import views
from rest_framework.response import Response

# Return first 5 largest company
def company(request):
    context = {'companies': Company.objects.annotate(total=Count('employees')).order_by('-total')[:5]}
    return render(request, 'resource_infor/company.html', context)

# Return employees list specific company
def employees_detail(request, company_pk):
    employees_list = Employees.objects.filter(company_id=company_pk)
    context = {'employees': employees_list}
    response = render(request, 'resource_infor/employees.html', context)
    return response

# Return  all company JSON format
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