from django.db import models
from food.models import Food
import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('food_photos', filename)


class Recipe(models.Model):
	"""docstring for Recipe"""

	name = models.CharField(max_length=100)
	brief = models.CharField(max_length=1000)
	ingredients = models.ManyToManyField(Food, through='Amount', verbose_name="list of ingredients")
	cover_image = models.ImageField(upload_to='photos/%Y/%m/%d', null=True);

	def __unicode__(self):
		return self.name


class Amount(models.Model):
	"""docstring for Amount"""
	
	ingredient = models.ForeignKey(Food)
	recipe = models.ForeignKey(Recipe)
	amount = models.CharField(max_length=50)

	def __unicode__(self):
		return self.recipe.name + self.ingredient.name
		
