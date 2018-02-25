from django.test import TestCase
from gov.models import Data
from django.urls import reverse

class DataestCase(TestCase):

    # Model Test #1
    def create_mast(self):
        Data.objects.create(
            property_name = 'Great Wall',
            property_address1 = '26 Ralphs Ride',
            property_address2 = 'Harmans Water',
            property_address3 = 'Bracknell',
            property_address4 = 'RG12 9EJ',
            unit_name = 'Elwyne\'s Unit',
            tenant_name = 'Elwyne',
            lease_start_date = "2001-01-01",
            lease_end_date = "2001-01-01",
            lease_years = 60,
            current_rent = 2000
    )

    # Model Test #2
    def test_string_representation(self):
        test = Data(tenant_name="Bob")
        self.assertEqual(str(test), test.tenant_name)

    # Views and Templates Test #1
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


