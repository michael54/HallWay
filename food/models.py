from django.db import models
from imagekit.models.fields import ProcessedImageField
from imagekit.processors import SmartResize, Adjust
import os
import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('food_photos', filename)

# Create your models here.

class FoodCategory(models.Model):
	"""Food Category Model"""
	name = models.CharField(db_index=True, max_length=100)
	parent = models.ForeignKey('self', null=True, blank=True)

	def __unicode__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		if self.id == 1:
			return ''
		else:
			return ('food_list', (), {'pk':self.id})



class Food(models.Model):
	"""Food Model, managing all kinds of food"""
	
	name = models.CharField(db_index=True, unique=True, max_length=100)
	category = models.ForeignKey(FoodCategory)
	brief = models.TextField(blank=True)
	cover_image = ProcessedImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=u'Cover image', processors=[Adjust(contrast=1.2, sharpness=1.1),
            SmartResize(300, 300)], format='JPEG', options={'quality': 90})
	
	storage_time = models.CharField(max_length=50, blank=True)
	storage_method = models.CharField(max_length=1000, blank=True)
	like_num = models.IntegerField(default=0)
	pick_method = models.TextField(blank=True, verbose_name=u'How to choose')
	food_efficacy = models.TextField(blank=True)
	view_num = models.IntegerField(default=0)
	

	def __unicode__(self):
		return self.name

	def active(self):
		if self.category_id == 1:
			return False
		else:
			return True

	@models.permalink
	def get_absolute_url(self):
		if self.category_id == 1:
			return ''
		else:
			return ('food_detail', (), {'pk': self.id})

	class Meta:
		ordering = ['like_num', 'view_num']



