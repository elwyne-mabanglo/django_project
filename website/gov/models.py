from django.db import models
from django.urls import reverse

class Data(models.Model):
    property_name = models.CharField(max_length=250)
    property_address1 = models.CharField(max_length=250)
    property_address2 = models.CharField(max_length=250)
    property_address3 = models.CharField(max_length=250)
    property_address4 = models.CharField(max_length=250)
    unit_name = models.CharField(max_length=250)
    tenant_name = models.CharField(max_length=250)
    lease_start_date = models.DateTimeField('lease start date')
    lease_end_date = models.DateTimeField('lease end date')
    lease_years = models.IntegerField(default=0)
    current_rent = models.FloatField(default=0)

    def __str__(self):
        return self.tenant_name