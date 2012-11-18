from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaLanguageBaseProfile
from recipe.models import Recipe

class MyProfile(UserenaLanguageBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')

    favourite_recipes = models.ManyToManyField(Recipe, blank=True,
    							related_name='favourite_recipes')

    
    location = models.CharField(max_length = 50, null = True, blank=True)
    age = models.PositiveSmallIntegerField(null = True, blank=True)
    website = models.URLField(null = True, blank=True)
    about_me = models.TextField(null = True, blank=True)
