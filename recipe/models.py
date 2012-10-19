from django.db import models
from django.contrib.auth.models import User
from food.models import Food
import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('Recipe_photos', filename)


class RecipeCategory(models.Model):
	"""docstring for RecipeCategory"""

	name = models.CharField(max_length=200)
	brief = models.CharField(max_length=2000)

	def __unicode__(self):
		return self.name


class Recipe(models.Model):
	"""docstring for Recipe"""

	name = models.CharField(max_length=200)
	author = models.ForeignKey(User)
	date = models.DateField(auto_now_add=True)
	category = models.ForeignKey(RecipeCategory)
	brief = models.CharField(max_length=2000)
	ingredients = models.ManyToManyField(Food, through='Amount', verbose_name=u"list of ingredients")
	cover_image = models.ImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=u'Cover image')
	tips = models.CharField(max_length=2000)
	did_num = models.IntegerField(default=0)
	like_num = models.IntegerField(default=0)
	view_num = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name


class Amount(models.Model):
	"""docstring for Amount"""
	
	ingredient = models.ForeignKey(Food)
	recipe = models.ForeignKey(Recipe)
	amount = models.CharField(max_length=50)
	must = models.BooleanField(default=False)

	def __unicode__(self):
		return u'Amount of %s in %s' % (self.ingredient.name, self.recipe.name)
		
class Step(models.Model):
	"""docstring for Steps"""

	recipe = models.ForeignKey(Recipe)
	step_num = models.IntegerField()
	description = models.CharField(max_length = 1000)
	step_image = models.ImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=u'Step Image')

	def __unicode__(self):
		return u'Step %d of %s' % (self.step_num, self.recipe.name)
