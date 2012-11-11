# tasks.py

from celery.task import PeriodicTask
from recipe.models import Recipe
from celery.task.schedules import crontab
from celery.task import task

class ProcessTrendTask(PeriodicTask):
	run_every = crontab(hour=0)
	alpha = 0.8

	def run(self, **kwargs):
		objects = Recipe.objects.all()
		for obj in objects:
			obj.trend_num = float(obj.trend_num) * alpha + float(obj.today_view_num) * (1-alpha)
			obj.today_view_num = 0
			obj.save()


@task(ignore_result=True)
def add_view_num(obj):
	obj.view_num = obj.view_num+1
	obj.save()
