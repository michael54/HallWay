"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django_dynamic_fixture import G
from food.models import Food, FoodCategory


class SimpleTest(TestCase):
	def test(self):
		food2 = G(FoodCategory)
		food1 = G(Food, FoodCategory=[food2,])
		
		print food1