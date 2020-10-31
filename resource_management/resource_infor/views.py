from django.shortcuts import render
from django.db.models import Count
from .models import Company, Employees
from rest_framework import views
from rest_framework.response import Response

# Return company list in html format
def company(request):
    return render(request,'resource_infor/company.html',{'company':Company.objects.all()})

# Return employees list in html format
def employees(request):
    return render(request,'resource_infor/employees.html',{'employees':Employees.objects.all()})

# Return company list in JSON format
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