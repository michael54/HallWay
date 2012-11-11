from recipe import recommendations, itemsim
from userena.views import profile_detail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from recipe.models import Recipe

def profile(request, username):
	user = get_object_or_404(User, username__iexact = username)
	rec = recommendations.getRecommendedItems(itemsim.critics, itemsim.itemsim, str(user.id))[0:10]
	id_list = []
	for (similarity, i) in rec:
		id_list.append(i)

	objects = Recipe.objects.filter(id__in=id_list)
	objects = dict([(obj.id, obj) for obj in objects])
	sorted_objects = [objects[id] for id in id_list]
	extra_context = dict()
	extra_context['recommends'] = sorted_objects

	response = profile_detail(request, username, extra_context = extra_context)
	return response