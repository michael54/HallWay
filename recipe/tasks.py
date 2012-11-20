# tasks.py

from celery.task import PeriodicTask
from recipe.models import Recipe, Vote
from celery.task.schedules import crontab
from celery.task import task
from django.contrib.auth.models import User
from datetime import timedelta
from actstream import action
from django.shortcuts import get_object_or_404
from django.contrib.comments.signals import comment_was_posted
from recipe.models import Recipe
from django.db.models.signals import post_save
from actstream.actions import follow, unfollow

def async_comment_posted(sender, comment=None, request=None, **kwargs):
	action.send(request.user, verb="discussed", action_object=comment, target=comment.content_object)

comment_was_posted.connect(async_comment_posted)


def recipe_saved(sender, instance=None, created=None, **kwargs):
	if created:
		action.send(instance.author, verb='created a new Recipe,', target = instance)
		follow(instance.author, instance, actor_only=False)

post_save.connect(recipe_saved, sender=Recipe)

class ProcessTrendTask(PeriodicTask):
	# run_every = crontab(hour=0)
	run_every = timedelta(hours = 1)

	def run(self, **kwargs):
		alpha = 0.8
		objects = Recipe.objects.only('trend_num', 'today_view_num').all()
		for obj in objects:
			obj.trend_num = float(obj.trend_num) * alpha + float(obj.today_view_num) * (1-alpha)
			obj.today_view_num = 0
			obj.save()


@task(ignore_result=True)
def add_view_num(obj):
	obj.view_num = obj.view_num+1
	obj.today_view_num = obj.today_view_num+1
	obj.save()



@task()
def get_or_create_vote(r, u, s, c):
	try:
		recipe_object = Recipe.objects.get(pk = r)
		user_object = User.objects.get(pk = u)
		v = Vote.objects.get(recipe = recipe_object, user = user_object)
	except Vote.DoesNotExist:
		v = Vote(recipe = recipe_object, user = user_object, score = s, comment = c)
		recipe_object.cumulative_score = recipe_object.cumulative_score + s
		recipe_object.rating_num = recipe_object.rating_num + 1
		v.save()
		action.send(user_object, verb='rated on', action_object = v, target = recipe_object)
	else:
		old_score = v.score
		v.score = s
		v.comment = c
		recipe_object.cumulative_score = recipe_object.cumulative_score + s - old_score
		v.save()

	return recipe_object.save()

@task()
def add_like_num(user, recipeid):
	recipe = get_object_or_404(Recipe, pk=recipeid)
	profile = user.get_profile()
	profile.favourite_recipes.add(recipe)
	action.send(user, verb='liked', target=recipe)
	recipe.like_num = recipe.like_num + 1
	return recipe.save()


@task()
def decrease_like_num(user, recipeid):
	recipe = get_object_or_404(Recipe, pk=recipeid)
	profile = user.get_profile()
	profile.favourite_recipes.remove(recipe)
	recipe.like_num = recipe.like_num - 1
	return recipe.save()