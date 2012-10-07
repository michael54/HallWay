from django.db import models


# Create your models here.


class Food(models.Model):
	"""docstring for Food"""
	
	name = models.CharField(max_length=50)
	brief = models.CharField(max_length=1000)
	storage_time = models.CharField(max_length=50)
	storage_method = models.CharField(max_length=1000)
	recipe_num = models.IntegerField()
	like_num = models.IntegerField()
	recipes = models.ManyToManyField('recipe.Recipe', verbose_name="list of recipes")

	def __unicode__(self):
		return self.name
