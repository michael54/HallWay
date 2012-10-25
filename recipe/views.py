# Create your views here.
from django.shortcuts import render


def nav(request):
	return render(request, 'nav.html')
