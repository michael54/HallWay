from django.db import models
from recipe.models import Amount

class ShoppingList(models.Model):
	""" Shopping List Model """

	amount = models.ManyToManyField(Amount, verbose_name=u'list of ingredients')
