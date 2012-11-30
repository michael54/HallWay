from django.core.management.base import BaseCommand
from recipe.models import Vote
from recipe import recommendations
import zipfile
import json

class Command(BaseCommand):
	help = 'Build recipe similarity table based on all votes'
	
	def handle(self, *args, **options):
		lastid = -1
		critics = {}
		# f = zipfile.ZipFile("recipe/itemsim.zip", mode = "w", compression = zipfile.ZIP_DEFLATED,)
		f = open("recipe/itemsim.py", "w+")
		for v in Vote.objects.all():
			if v.user.id not in critics:
				critics[v.user.id] = {}
			critics[v.user.id][v.recipe.id] = float(v.score)

		itemsim = recommendations.calculateSimilarItems(critics, n=10)
		# f.writestr('itemsim.py', "critics = "+json.dumps(critics)+"\n"+"itemsim = "+json.dumps(itemsim))
		f.write("critics = "+json.dumps(critics)+"\n"+"itemsim = "+json.dumps(itemsim))
		f.close()
