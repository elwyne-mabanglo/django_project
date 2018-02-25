from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Data
import logging
import re, csv
from django.db.models import Sum
from django.db.models import Count
from datetime import datetime

class CountView(generic.ListView):
    template_name = 'gov/tenant.html'
    context_object_name = 'all_data'

    def get_queryset(self):
        tenant_list = Data.objects.all().values('tenant_name').annotate(total=Count('tenant_name'))

        aggregated_tenants = {
            'Arqiva': [],
            'Cornerstone': [],
            'Everything_Everywhere': [],
            'Everything_Everywhere_and_Hutchinsion': [],
            'O2': [],
            'Vodafone': []
        }

        for tenant_and_masts in tenant_list:
            name = tenant_and_masts['tenant_name']
            if 'Arqiva' in name:
                aggregated_tenants['Arqiva'].append(tenant_and_masts)
            elif 'Cornerstone' in name:
                aggregated_tenants['Cornerstone'].append(tenant_and_masts)
            elif '&' in name:
                aggregated_tenants['Everything_Everywhere_and_Hutchinsion'].append(tenant_and_masts)
            elif 'Everything' in name:
                aggregated_tenants['Everything_Everywhere'].append(tenant_and_masts)
            elif 'O2' in name:
                aggregated_tenants['O2'].append(tenant_and_masts)
            elif 'Vodafone' in name:
                aggregated_tenants['Vodafone'].append(tenant_and_masts)

        all = [];
        for aggregated_tenant in aggregated_tenants:
            tenant_and_mast = {
                'tenant_name': aggregated_tenant,
                'total': 0
            }
            for tenant_and_masts in aggregated_tenants[aggregated_tenant]:
                tenant_and_mast['total'] += tenant_and_masts['total']
            all.append(tenant_and_mast)

        return all;
  

class IndexView(generic.ListView):
    template_name = 'gov/index.html'
    context_object_name = 'all_data'

    def get_queryset(self):
        return [
            Data.objects.order_by("lease_years") ,
            Data.objects.aggregate(Sum('current_rent'))
        ]

class LeaseDateView(generic.ListView):
    template_name = 'gov/lease_date.html'
    context_object_name = 'all_data'

    def get_queryset(self):


        format = '%d-%b-%y'
        start_date = datetime.strptime("01-Jun-90", format)
        end_date = datetime.strptime("31-Mar-07", format)

        return Data.objects.filter(lease_start_date__range=(start_date, end_date))

class DescView(generic.ListView):
    template_name = 'gov/top.html'
    context_object_name = 'all_data'

    def get_queryset(self):
        return Data.objects.order_by("-lease_years")[:5]

class AscView(generic.ListView):
    template_name = 'gov/top.html'
    context_object_name = 'all_data'

    def get_queryset(self):
        return Data.objects.order_by("lease_years")[:5]

class DataCreate(CreateView):
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
    if not csv_file.name.endswith('.csv'):
        return HttpResponseRedirect(reverse("gov:upload_csv"))

    #if file is too large, return
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

            try:
                 #format dates
                format = '%d-%b-%y'
                start_date = datetime.strptime(row[7], format)
                end_date = datetime.strptime(row[8], format)
            except:
                return HttpResponse(row[7] + " " + row[8])

  
            def clean(field):
                return field.strip()


            #def normalise_tenant_name(name):
            #    normalised_name =  re.sub(r'(?i)UK|\.|Services ', '', name) #name.replace(r'UK|\.|Services ', '')
            #    return normalised_name

            #tenant_exist = Data.objects.filter(tenant_name__icontains=row[6])
            ## doesnt really work because it's not LIKE

            #if len(tenant_exist) > 1:
            #    tenant_exist = tenant_exist[0]
            #else:
            #    tenant_exist = row[6]


            #tenant = clean(row[6])

            #if tenant.findall("&"):



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
  
    return HttpResponseRedirect(reverse("gov:index"))

    