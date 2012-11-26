# search.py
from django.shortcuts import render_to_response, render
from django.http import Http404
from recipe.models import Recipe
from food.models import Food
from recipe.forms import SearchForm
from django.forms.formsets import formset_factory
import sys

def autonav(request):
	if request.is_ajax():
		q = request.POST['q']
		queries = {}
		queries['recipe'] = Recipe.objects.filter(name__contains= q).only('name','cover_image','brief')[:3]
		queries['food'] = Food.objects.filter(name__contains=q).only('name','cover_image','brief')[:3]
		
		return render_to_response('autocomplete.html',{'recipe_list':queries['recipe'], 'food_list':queries['food']})

def advanced_search(request):
	SearchFormSet = formset_factory(SearchForm, extra = 3)
	if request.method == 'POST':
		pass
	else:
		search_formset = SearchFormSet()
		return render(request, 'recipe/advanced_search.html', {'formset':search_formset})

def normal_search(request):
	if request.is_ajax():
		q = request.POST['q']
		results = Recipe.objects.filter(name__contains = q).only('name', 'cover_image', 'like_num')
		return render_to_response('recipe/result.html', {'results': results})
	else:
		raise Http404