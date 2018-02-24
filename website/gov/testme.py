import os
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.db.models import Data
import logging

f=open(os.path.normpath("C:/Users/Elwyne/Downloads/Mobile Phone Masts.csv"),'r')
# a = f.read()

####################

file_data = f.read()   

lines = file_data.split("\n")


for line in lines[1:]:        

    fields = line.split(",")

    m = Data(property_name = fields[0].strip(),
                property_address1 = fields[1].strip(),
                property_address2 = fields[2].strip(),
                property_address3 = fields[3].strip(),
                property_address4 = fields[4].strip(),
                unit_name = fields[5].strip(),
                tenant_name = fields[6].strip(),
                lease_start_date = "",
                lease_end_date = "",
                lease_years = "",
                current_rent = ""
                )
    try:         
        m.save()
    except:
        print(f'line: {line}, fields: {fields}')

f.close()
