from userena.views import profile_detail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from recipe.models import Recipe

def profile(request, username):
	user = get_object_or_404(User, username__iexact = username)
	
	response = profile_detail(request, username)
	return response