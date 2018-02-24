from django.db import models
from django.urls import reverse
import datetime

class Data(models.Model):
    property_name = models.CharField(default="",max_length=1000, blank=True)
    property_address1 = models.CharField(default="",max_length=1000, blank=True)
    property_address2 = models.CharField(default="",max_length=1000, blank=True)
    property_address3 = models.CharField(default="",max_length=1000, blank=True)
    property_address4 = models.CharField(default="",max_length=1000, blank=True)
    unit_name = models.CharField(default="",max_length=1000,blank=True)
    tenant_name = models.CharField(default="",max_length=1000,blank=True)
    lease_start_date = models.DateField(default=datetime.date.today,blank=True)
    lease_end_date = models.DateField(default=datetime.date.today,blank=True)
    lease_years = models.IntegerField(default=0,blank=True)
    current_rent = models.FloatField(default=0.0,blank=True)

    def __str__(self):
        return self.tenant_name

