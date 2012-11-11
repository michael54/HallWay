from django.db import models
from django.contrib.auth.models import User
from food.models import Food
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFit, Adjust
from django.core.validators import MaxValueValidator
import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('Recipe_photos', filename)


class RecipeCategory(models.Model):
	"""docstring for RecipeCategory"""

	name = models.CharField(max_length=200)
	brief = models.TextField()

	def __unicode__(self):
		return self.name


class Recipe(models.Model):
	"""docstring for Recipe"""

	name = models.CharField(max_length=200)
	author = models.ForeignKey(User)
	date = models.DateField(auto_now_add=True)
	category = models.ForeignKey(RecipeCategory)
	brief = models.TextField()
	ingredients = models.ManyToManyField(Food, through='Amount', verbose_name=u"list of ingredients")

	cover_image = ProcessedImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=u'Cover image',
						processors=[Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFit(width=640,upscale=True)], format='JPEG', options={'quality': 90})

	tips = models.TextField(blank=True)
	did_num = models.PositiveIntegerField(default=0)
	like_num = models.PositiveIntegerField(default=0)
	view_num = models.PositiveIntegerField(default=0)
	prep_time = models.TimeField()
	cook_time = models.TimeField()

	cumulative_score = models.PositiveIntegerField(default=0)
	rating_num = models.PositiveIntegerField(default=0)


	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('recipe_detail', (), {'pk': self.id})

	class Meta:
		ordering = ['view_num', 'like_num']


class DidRecipe(models.Model):
	"""docstring for DidRecipe"""
	recipe = models.ForeignKey(Recipe)
	user = models.ForeignKey(User)
	image = ProcessedImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=u'Cover image',
						processors=[Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFit(width=640,upscale=True)], format='JPEG', options={'quality': 90})
	comments = models.TextField()



class Amount(models.Model):
	"""docstring for Amount"""
	
	ingredient = models.ForeignKey(Food)
	recipe = models.ForeignKey(Recipe)
	amount = models.CharField(max_length=50)
	must = models.BooleanField(default=False)

	def __unicode__(self):
		return u'Amount of %s in %s' % (self.ingredient.name, self.recipe.name)

	class Meta:
		ordering = ['recipe']
		unique_together = ('recipe', 'ingredient')
		
class Step(models.Model):
	"""docstring for Steps"""

	recipe = models.ForeignKey(Recipe)
	step_num = models.PositiveIntegerField()
	description = models.CharField(max_length = 1000)
	step_image = models.ImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=u'Step Image')

	def __unicode__(self):
		return u'Step %d of %s' % (self.step_num, self.recipe.name)

	class Meta:
		ordering = ['recipe', 'step_num']
		unique_together = ("recipe", "step_num")


class Vote(models.Model):
	"""Vote class, used for recommendation system """
	recipe = models.ForeignKey(Recipe)
	user = models.ForeignKey(User)
	score = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])

	def __unicode__(self):
		return u'Vote for %s from %s' %(self.recipe.name, self.user)

	class Meta:
		ordering = ['user']
		unique_together = ("user", "recipe")












