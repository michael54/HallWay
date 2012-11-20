from __future__ import absolute_import

from django import http
from django.conf import settings
from django.contrib import comments
from django.contrib.comments import signals
from django.contrib.comments.views.utils import next_redirect, confirmation_view
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape

from django.utils import simplejson
import sys

def post_comment(request, next=None, using=None):
    if request.is_ajax():
        
        # Fill out some initial data fields from an authenticated user, if present
        data = request.POST.copy()
        if request.user.is_authenticated():
            if not data.get('name', ''):
                data["name"] = request.user.get_full_name() or request.user.get_username()
            if not data.get('email', ''):
                data["email"] = request.user.email

        # Look up the object we're trying to comment about
        ctype = data.get("content_type")
        object_pk = data.get("object_pk")
        
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.using(using).get(pk=object_pk)
        # Construct the comment form
        form = comments.get_form()(target, data=data)

        # Otherwise create the comment
        comment = form.get_comment_object()
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        if request.user.is_authenticated():
            comment.user = request.user

        # Signal that the comment is about to be saved
        responses = signals.comment_will_be_posted.send(
            sender=comment.__class__,
            comment=comment,
            request=request
        )

        # Save the comment and signal that it was saved
        comment.save()
        signals.comment_was_posted.send(
            sender=comment.__class__,
            comment=comment,
            request=request
        )

        return render_to_response('recipe/comment.html', {'comment': comment})
    else:
        raise http.Http404