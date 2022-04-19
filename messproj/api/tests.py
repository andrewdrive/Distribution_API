from django.test import TestCase
from .models import Distribution
from django.utils import timezone


class DistributionTestCase(TestCase):
     def setUp(self) -> None:
          Distribution.objects.create(
             start_datetime=...
          )

     





# Create your tests here.
