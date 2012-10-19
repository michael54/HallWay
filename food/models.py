from django.db import models
import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('food_photos', filename)

# Create your models here.

class FoodCategory(models.Model):
	"""Food Category Model"""
	name = models.CharField(max_length=100)

	def __unicode__(self):
		return self.name


class Food(models.Model):
	"""Food Model, managing all kinds of food"""
	
	name = models.CharField(max_length=100)
	category = models.ForeignKey(FoodCategory)
	brief = models.CharField(max_length=1000)
	cover_image = models.ImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=u'Cover image')
	storage_time = models.CharField(max_length=50, blank=True)
	storage_method = models.CharField(max_length=1000, blank=True)
	recipe_num = models.IntegerField(default=0)
	like_num = models.IntegerField(default=0)
	pick_method = models.CharField(max_length=1000, blank=True, verbose_name=u'How to choose')
	food_efficacy = models.CharField(max_length=1000, blank=True)


	def __unicode__(self):
		return self.name
