from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Data
import re, csv
from django.db.models import Sum
from django.db.models import Count
from datetime import datetime

class CountView(generic.ListView):
    template_name = 'gov/tenant.html'
    context_object_name = 'all_data'

    def get_queryset(self):

        # get count data by tenant
        tenant_list = Data.objects.all().values('tenant_name').annotate(total=Count('tenant_name'))

        # create object with tenants
        aggregated_tenants = {
            'Arqiva Services Ltd': [],
            'Cornerstone Telecommunications Infrastructure': [],
            'Everything Everywhere Ltd': [],
            'Everything Everywhere Ltd & Hutchinson 3G UK': [],
            'O2 (UK) Ltd': [],
            'Vodafone Ltd': []
        }

        # match tenant list with string and append data to object
        for tenant_and_masts in tenant_list:
            name = tenant_and_masts['tenant_name']
            if 'Arqiva' in name:
                aggregated_tenants['Arqiva Services Ltd'].append(tenant_and_masts)
            elif 'Cornerstone' in name:
                aggregated_tenants['Cornerstone Telecommunications Infrastructure'].append(tenant_and_masts)
            elif '&' in name:
                aggregated_tenants['Everything Everywhere Ltd & Hutchinson 3G UK'].append(tenant_and_masts)
            elif 'Everything' in name:
                aggregated_tenants['Everything Everywhere Ltd'].append(tenant_and_masts)
            elif 'O2' in name:
                aggregated_tenants['O2 (UK) Ltd'].append(tenant_and_masts)
            elif 'Vodafone' in name:
                aggregated_tenants['Vodafone Ltd'].append(tenant_and_masts)

        all = [];

        # combine tenates values and store in all
        for aggregated_tenant in aggregated_tenants:
            tenant_and_mast = {
                'tenant_name': aggregated_tenant,
                'total': 0
            }
            for tenant_and_masts in aggregated_tenants[aggregated_tenant]:
                tenant_and_mast['total'] += tenant_and_masts['total']
            all.append(tenant_and_mast)

        return [all, # all tenants with total value 
                Data.objects.aggregate(Sum('current_rent'))]; # query sum rent
  
class IndexView(generic.ListView):
    template_name = 'gov/index.html'
    context_object_name = 'all_data'
    def get_queryset(self):
        return [
            Data.objects.order_by("lease_years") , # query aAll data order by ascending
            Data.objects.aggregate(Sum('current_rent')) # query sum rent
        ]

class LeaseDateView(generic.ListView):
    # view returns data between 01-Jine-99 and 31-Aug-07 and total rent
    template_name = 'gov/lease_date.html'
    context_object_name = 'all_data'
    def get_queryset(self):       
        format = '%d-%b-%y' # data format
        start_date = datetime.strptime("01-Jun-99", format) # start date
        end_date = datetime.strptime("31-Aug-07", format) # end date
        return [Data.objects.filter(lease_start_date__range=(start_date, end_date)), # query data between
                Data.objects.aggregate(Sum('current_rent'))] # query sum rent

class DescView(generic.ListView):
    # view returns lease years in order of descending limited by 5 and total rent
    template_name = 'gov/top.html' 
    context_object_name = 'all_data'
    def get_queryset(self):
        return [Data.objects.order_by("-lease_years")[:5], # query lease descending limited 5
                Data.objects.aggregate(Sum('current_rent'))] # query sum rent

class AscView(generic.ListView):
    # view returns lease years in order of ascending limited by 5 and total rent
    template_name = 'gov/top.html'
    context_object_name = 'all_data'
    def get_queryset(self):
        return [Data.objects.order_by("lease_years")[:5], # query lease ascending limited 5
                Data.objects.aggregate(Sum('current_rent'))] # query sum rent

class DataCreate(CreateView):
    # view for creating a display form for adding new data
    model = Data
    fields = ['property_name','property_address1','property_address2','property_address3','property_address4',
              'unit_name','tenant_name','lease_start_date','lease_end_date','lease_years','current_rent']
    success_url = reverse_lazy('gov:index')

def upload_csv(request):
    data = {}

    if "GET" == request.method:
        return render(request, "gov/upload_csv.html", data)
    # if not GET, then proceed

    csv_file = request.FILES["csv_file"]

    # check file type
    if not csv_file.name.endswith('.csv'):
        return HttpResponseRedirect(reverse("gov:upload_csv"))

    # check file size
    if csv_file.multiple_chunks():
        return HttpResponseRedirect(reverse("gov:upload_csv"))
    

    file_data = csv_file.read().decode("utf-8")     

    lines = file_data.split("\r\n")

    reader = csv.reader(lines, skipinitialspace=True)

    # skip header
    next(reader)

    for row in reader:

        # ignore first row
        if len(row) > 1:

 
             # format dates
            format = '%d-%b-%y'
            start_date = datetime.strptime(row[7], format)
            end_date = datetime.strptime(row[8], format)


            # clean fields
            def clean(field):
                return field.strip()

            # store in Data object
            m = Data(
                property_name = clean(row[0]),
                property_address1 = clean(row[1]),
                property_address2 = clean(row[2]),
                property_address3 = clean(row[3]),
                property_address4 = clean(row[4]),
                unit_name = clean(row[5]),
                tenant_name = clean(row[6]),
                lease_start_date = start_date,
                lease_end_date = end_date,
                lease_years = row[9],
                current_rent = row[10]
            )

            m.save()
    
    # return to home page
    return HttpResponseRedirect(reverse("gov:index"))

    