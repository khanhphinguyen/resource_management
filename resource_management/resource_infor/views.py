from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render, HttpResponse
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Company, Employees
from rest_framework import views
from rest_framework.response import Response

# Return company list in html format
def company(request):
    return render(request,'resource_infor/company.html',{'company':Company.objects.all()})

# Return employees list in html format
@csrf_exempt
@cache_page(900)
@require_http_methods(['GET', 'POST'])
def employees(request):
    if request.method == 'GET':
        employeeslist = tuple(Employees.objects.values_list('employee_name',flat=True))
        paginator = Paginator(employeeslist, 2)
        pages = request.GET.get('page', 1)
        try:
            employeeslist = paginator.page(pages)
        except PageNotAnInteger:
            employeeslist = paginator.page(1)
        response = render(request,'resource_infor/employees.html',{'employees':employeeslist})

        if request.COOKIES.get('visits'):
            value = int(request.COOKIES.get('visits'))
            print('Get cookies')
            response.set_cookie('visits',value + 1)
        else:
            value = 1
            print('Set cookies')
            response.set_cookie('visits', value)
        return response
    elif request.method == 'POST':
        return HttpResponse('POST method was not support')

# Return company list in JSON format
# test git
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