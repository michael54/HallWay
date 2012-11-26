# search.py
from django.shortcuts import render_to_response
from recipe.models import Recipe
from food.models import Food
from recipe.forms import SearchForm
from django.forms.formsets import formset_factory

def autonav(request):
	if request.is_ajax():
		data = ''
		q = request.POST['q']
		queries = {}
		queries['recipe'] = Recipe.objects.filter(name__contains= q)[:3]
		queries['food'] = Food.objects.filter(name__contains=q)[:3]
		print>>sys.stderr, queries
		return render_to_response('autocomplete.html',{'recipe_list':queries['recipe'], 'food_list':queries['food']})

def advanced_search(request):
	SearchFormSet = formset_factory(SearchForm, extra = 3)
	if request.method == 'POST':
		pass
	else:
		search_formset = SearchFormSet()
		return render(request, 'recipe/advanced_search.html', {'formset':search_formset})