# search.py
from django.shortcuts import render_to_response, render
from django.http import Http404
from recipe.models import Recipe, Amount, RecipeCategory
from food.models import Food
from recipe.forms import SearchForm
from django.forms.formsets import formset_factory
from django.db.models import Q
import sys
from django.core.paginator import Paginator

def autonav(request):
	if request.is_ajax():
		q = request.POST['q']
		queries = {}
		queries['recipe'] = Recipe.objects.filter(name__contains= q).only('name','cover_image','brief')[:3]
		queries['food'] = Food.objects.filter(name__contains=q).only('name','cover_image','brief')[:3]
		
		return render_to_response('autocomplete.html',{'recipe_list':queries['recipe'], 'food_list':queries['food']})

result_list = list()

def advanced_search(request):
	SearchFormSet = formset_factory(SearchForm, extra = 3)
	if request.method == 'POST':
		result_list = list()
		search_formset = SearchFormSet(request.POST)
		if search_formset.is_valid():
			ingredient_list = list()
			for form in search_formset:
				ingredient_list.append(form.cleaned_data['ingredient'])
			amount_list = list(Amount.objects.filter(ingredient__name__in=ingredient_list, must=True).only('recipe'))
			candidate_list = list()
			for a in amount_list:
				if a.recipe not in candidate_list:
					candidate_list.append(a.recipe)
			for r in candidate_list:
				rl = list(r.amount_set.filter(must = True))
				flag = True
				for i in rl:
					if i.ingredient.name not in ingredient_list:
						flag = False
						break
				if flag:
					result_list.append(r)

			paginator = Paginator(result_list, 10)

			return render(request, 'recipe/advanced_search_list.html', {
				'recipe_list': paginator.page(1),
				'Courses': RecipeCategory.objects.filter(parent__name='Courses').only('name'),
				'Cuisines': RecipeCategory.objects.filter(parent__name='Cuisines').only('name'),
				'Main_Ingredients': RecipeCategory.objects.filter(parent__name='Main Ingredients').only('name'),
				'Special_Diets': RecipeCategory.objects.filter(parent__name='Special Diets').only('name'),
				})
	else:
		if 'page' in request.GET:
			page = request.GET['page']
			paginator = Paginator(result_list, 10)
			return render(request, 'recipe/advanced_search_list.html', {
				'recipe_list': paginator.page(page),
				'Courses': RecipeCategory.objects.filter(parent__name='Courses').only('name'),
				'Cuisines': RecipeCategory.objects.filter(parent__name='Cuisines').only('name'),
				'Main_Ingredients': RecipeCategory.objects.filter(parent__name='Main Ingredients').only('name'),
				'Special_Diets': RecipeCategory.objects.filter(parent__name='Special Diets').only('name'),
				})
		else:
			search_formset = SearchFormSet()
			return render(request, 'recipe/advanced_search.html', {'formset':search_formset})

def normal_search(request):
	if request.is_ajax():
		q = request.POST['q']
		results = list(Recipe.objects.filter(Q(name__contains = q)|Q(ingredients__name__contains = q)).distinct().only('name', 'cover_image', 'like_num'))
		return render_to_response('recipe/result.html', {'results': results})
	else:
		raise Http404