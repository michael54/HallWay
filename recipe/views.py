# Create your views here.
from django.shortcuts import render
from userena.views import signin


def nav(request):
	return render(request, 'nav.html')

