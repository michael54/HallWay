# Create your views here.
from django.shortcuts import render

def nav(request):
	return render(request, 'base.html', content_type="application/xhtml+xml")
