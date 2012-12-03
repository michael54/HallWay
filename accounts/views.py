from userena.views import profile_detail
from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404, render_to_response, redirect
from recipe.models import Recipe
from actstream import models as ActStream
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from userena.contrib.umessages.models import Message, MessageRecipient
from userena.utils import get_profile_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from guardian.decorators import permission_required_or_403
from userena.decorators import secure_required
from actstream import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from accounts.forms import MugshotForm
from userena.signals import signup_complete
from django.dispatch import receiver
from recipe import recommendations


import sys
import json

@login_required
def profile(request, username):
	user = get_object_or_404(User, username__iexact = username)
	if request.is_ajax():
		queryset = Message.objects.get_conversation_between(user, request.user)
		paginator = Paginator(queryset, 10)
		page = request.GET.get('page')
		try:
			message_list = paginator.page(page)
		except PageNotAnInteger:
			raise Http404
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			message_list = paginator.page(paginator.num_pages)
		return render_to_response('umessages/conversation.html',{'message_list': message_list})
	else:
		extra_context = dict()
		extra_context['followers'] = ActStream.followers(user)
		extra_context['followings'] = ActStream.following(user)
		extra_context['recipe_list'] = list(user.recipe_set.all().only('name', 'cover_image', 'did_num', 'like_num', 'date', 'view_num'))
		extra_context['favourite_list'] = list(user.get_profile().favourite_recipes.all().only('name', 'cover_image', 'did_num', 'like_num', 'date', 'view_num'))
		extra_context['form'] = MugshotForm()
		response = profile_detail(request, username, extra_context = extra_context)

		return response

@login_required
def leave_message(request, username):
	if request.is_ajax():
		user = get_object_or_404(User, username__iexact = username)
		msg = Message.objects.send_message(request.user, [user, ], str(request.POST['message']))
		if msg:
			return render_to_response('umessages/message.html', {'message': msg})
		else:
			return HttpResponse('Failed')
	else:
		raise Http404



@secure_required
@permission_required_or_403('change_profile', (get_profile_model(), 'user__username', 'username'))
def profile_edit(request, username):

	user = get_object_or_404(User, username__iexact=username)
	if(request.user != user):
		raise Http404
	profile = user.get_profile()

	if request.is_ajax():
		field = request.POST['field']
		value = request.POST['value']
		if field == 'first_name':
			user.first_name = value
			user.save()
			return HttpResponse('Saved!')
		elif field == 'last_name':
			user.last_name = value
			user.save()
			return HttpResponse('Saved!')
		elif field == 'location':
			profile.location = value
			profile.save()
			return HttpResponse('Saved!')
		elif field == 'age':
			profile.age = value
			profile.save()
			return HttpResponse('Saved!')
		elif field == 'website':
			profile.website = value
			profile.save()
			return HttpResponse('Saved!')
		elif field == 'about_me':
			profile.about_me = value
			profile.save()
			return HttpResponse('Saved!')
		return HttpResponse('Failed!')
	elif request.method == 'POST':
		form = MugshotForm(request.POST, request.FILES, instance = profile )
		if form.is_valid():
			form.save();
			return redirect('userena_profile_detail', username=username)
		else:
			return HttpResponse('Failed!')
	else:
		raise Http404

def message_comet(request):
	if request.is_ajax() and request.user.is_authenticated():
		number = MessageRecipient.objects.count_unread_messages_for(request.user)
		if number > 0:
			return render_to_response('umessages/notification.html', {'number': number})
		else:
			return HttpResponse('')
	else:
		raise Http404

@login_required
def activity(request):
	if request.is_ajax():

		queryset = models.user_stream(request.user)
		paginator = Paginator(queryset, 10)
		page = request.GET.get('page')
		try:
			action_list = paginator.page(page)
		except PageNotAnInteger:
			raise Http404
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			action_list = paginator.page(paginator.num_pages)
		return render_to_response('actstream/update_list.html',{
			'action_list': action_list,
		})

	else:
		queryset = models.user_stream(request.user)
		paginator = Paginator(queryset, 10)
		try:
			action_list = paginator.page(1)
		except PageNotAnInteger:
			raise Http404
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			action_list = paginator.page(paginator.num_pages)		
		return render(request, 'actstream/update.html', {
					'ctype': ContentType.objects.get_for_model(User),
					'actor': request.user, 
					'action_list': action_list,
					'following': models.following(request.user),
					'followers': models.followers(request.user),
					'recommends': recommendations.recommendRecipeForUser(request.user.id, 10)
			})


@receiver(signup_complete)
def set_default_mugshot(sender, user, **kwargs):
	profile = user.get_profile()
	profile.mugshot = 'no_mugshot.jpg'
	profile.save()

