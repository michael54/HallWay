from django.db import models

from food.models import Food

# Create your models here.



class Recipe(models.Model):
	"""docstring for Recipe"""

	name = models.CharField(max_length=100)
	brief = models.CharField(max_length=1000)
	ingredients = models.ManyToManyField(Food, through='Amount', verbose_name="list of ingredients")


	def __unicode__(self):
		return self.name


class Amount(models.Model):
	"""docstring for Amount"""
	def __init__(self, arg):
		super(Amount, self).__init__()
		self.arg = arg

	ingredient = models.ForeignKey(Food)
	recipe = models.ForeignKey(Recipe)
	amount = models.CharField(max_length=50)
		
