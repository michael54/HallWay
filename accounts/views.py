from userena.views import profile_detail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from recipe.models import Recipe
from actstream import models as ActStream

def profile(request, username):
	user = get_object_or_404(User, username__iexact = username)
	
	extra_context = dict()
	extra_context['followers'] = ActStream.followers(request.user)
	extra_context['following'] = ActStream.following(request.user)

	
	response = profile_detail(request, username, extra_context = extra_context)

	return response