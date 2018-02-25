from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Data
import logging
import sys
import csv

class IndexView(generic.ListView):
    template_name = 'gov/index.html'
    context_object_name = 'all_data'

    def get_queryset(self):
        return Data.objects.all()

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
    
    for line in lines[1:]:        

        fields = line.split(",")
        
        if (len(fields) > 1):

            #try:
            m = Data(
                property_name = fields[0],
                property_address1 = fields[1],
                property_address2 = fields[2],
                property_address3 = fields[3],
                property_address4 = fields[4],
                unit_name = fields[5],
                tenant_name = fields[6],
                lease_start_date = "2012-01-02", #fields[7],
                lease_end_date = "2012-01-02", #fields[8],
                lease_years = fields[9],
                current_rent = fields[10]
            )
         
            m.save()
            #except:
            #    err = sys.exc_info()[0]
            #    return HttpResponse(f'line: {line} ; fields: {fields}, error: {err}')

    return HttpResponseRedirect(reverse("gov:index"))
