from userena.views import profile_detail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render_to_response
from recipe.models import Recipe
from actstream import models as ActStream
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from userena.contrib.umessages.models import Message
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


