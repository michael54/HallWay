import sys
import shutil
import os
import uuid
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from recipe.models import Recipe, RecipeCategory, Vote, Step, Amount
from recipe.forms import RecipeForm, VoteForm, StepForm, AmountForm, DidRecipeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView
from recipe import recommendations
from recipe.tasks import add_view_num, get_or_create_vote, add_like_num, decrease_like_num
from django.core.urlresolvers import reverse
from food.models import Food, FoodCategory
from django.core import serializers
from actstream import action
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.conf import settings
from accounts.models import MyProfile
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.easythumbnails import EasyThumbnailUploadBackend
from recipe.search import autonav, normal_search

did_image_upload = AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(540,000), QUALITY=90, DETAIL = False, SHARPEN = False,UPLOAD_DIR='Recipe_Images/Did_Images')

cover_image_upload = AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(540,000), QUALITY=90, DETAIL = False, SHARPEN = False,UPLOAD_DIR='Recipe_Images/Cover_Images')

step_image_upload = AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(540,000), QUALITY=80, DETAIL = False, SHARPEN = False,UPLOAD_DIR='Recipe_Images/Step_Image')

def nav(request):
	return render(request, 'nav.html')

def index(request):
	if request.is_ajax():
		return autonav(request)
	else:
		return render(request, 'index.html')

class RecipeDetailView(DetailView):

	def get_object(self):
		object = Recipe.objects.select_related().get(id=self.kwargs.get('pk',None))

		add_view_num.delay(object)

		return object

	def get_context_data(self, **kwargs):
		context = super(RecipeDetailView, self).get_context_data(**kwargs)
		
		context['recommends'] = recommendations.recommendRecipeForRecipe(context['object'].id, 10)

		if self.request.user.is_authenticated():
			try:
				vote = Vote.objects.get(recipe = context['object'], user=self.request.user)
			except Vote.DoesNotExist:
				context['vote'] = None
			else:
				context['vote'] = vote

		context['profile'] = MyProfile.objects.only('mugshot').get(user = context['object'].author)
		context['liked'] = context['profile'].favourite_recipes.filter(id=context['object'].id).only('id')

		context['amount_list'] = Amount.objects.filter(recipe = context['object']).select_related('ingredient').only('ingredient__name')
		context['step_list'] = Step.objects.filter(recipe = context['object']).order_by('step_num')
		context['votelist'] = Vote.objects.filter(recipe = context['object']).order_by('-date')
		return context

class RecipeCategoryListView(ListView):
	context_object_name = "recipe_list"
	paginate_by = 10

	def get_queryset(self):		
		if self.args[1] == 'hot':
			self.recipecategory = get_object_or_404(RecipeCategory, id__iexact=self.args[0])
			return Recipe.objects.filter(category = self.recipecategory)
		elif self.args[1] == 'time':
			self.recipecategory = get_object_or_404(RecipeCategory, id__iexact=self.args[0])
			return Recipe.objects.filter(category = self.recipecategory).order_by("-date")
		elif self.args[1] == 'trend':
			self.recipecategory = get_object_or_404(RecipeCategory, id__iexact=self.args[0])
			return Recipe.objects.filter(category = self.recipecategory).order_by("-trend_num")
		else:
			raise Http404

	def get_context_data(self, **kwargs):
		context = super(RecipeCategoryListView, self).get_context_data(**kwargs)
		context['category'] = self.recipecategory
		context['Courses'] = RecipeCategory.objects.filter(parent__name='Courses').only('name')
		context['Cuisines'] = RecipeCategory.objects.filter(parent__name='Cuisines').only('name')
		context['Main_Ingredients'] = RecipeCategory.objects.filter(parent__name='Main Ingredients').only('name')
		context['Special_Diets'] = RecipeCategory.objects.filter(parent__name='Special Diets').only('name')
		return context

class HotRecipeListView(ListView):
	queryset = Recipe.objects.all()
	context_object_name = "hot_recipe_list"
	template_name = "recipe/hot_recipe_list.html"
	paginate_by = 10

@login_required
def rate(request, pk):
	if request.is_ajax():
		user = request.user.id
		form = VoteForm(request.POST)
		if form.is_valid():
			score = form.cleaned_data['score']
			comment = form.cleaned_data['comment']
			get_or_create_vote.delay(pk, user, score, comment)
			return HttpResponse('<div id="ajax-feedback">Success</div>')
		else:
			return HttpResponse('<div id="ajax-feedback">Failed</div>')
	else:
		raise Http404


@login_required
def like(request, pk):
	"""
	Handle ajax request to like a recipe from a user 
	"""
	if request.is_ajax():
		
		add_like_num.delay(request.user, pk)

		return HttpResponse('Liked')
	else:
		raise Http404	


@login_required
def unlike(request, pk):
	"""
	Handle ajax request to unlike a recipe from a user 
	"""
	if request.is_ajax():
		decrease_like_num.delay(request.user, pk)

		return HttpResponse('Liked')
	else:
		raise Http404	


@login_required
def recipe_create(request):
	"""
	Page for create a new recipe
	"""    
	AmountFormSet = formset_factory(AmountForm, extra = 1)
	StepFormSet = formset_factory(StepForm, extra = 1)
	if request.method == 'POST':
		recipe_form = RecipeForm(request.POST)
		amount_formset = AmountFormSet(request.POST, prefix='amount')
		step_formset = StepFormSet(request.POST, prefix='step')
		if recipe_form.is_valid() and amount_formset.is_valid() and step_formset.is_valid():
			r = recipe_form.save()
			step = 0
			for form in step_formset:
				des = ''
				if 'description' in form.cleaned_data:
					des = form.cleaned_data['description']
				else:
					continue
				s = Step(recipe = r, step_num = step, description = des)
				s.step_image = form.cleaned_data['step_image'];
				s.save()
				step = step + 1

			unactive = get_object_or_404(FoodCategory, pk = 1)
			for form in amount_formset:
				if 'ingredient' in form.cleaned_data:
					f, created = Food.objects.get_or_create(name = form.cleaned_data['ingredient'], defaults={'category': unactive})
					a = Amount(ingredient = f, recipe = r, amount = form.cleaned_data['amount'], must = form.cleaned_data['must'])
					a.save()
				else:
					continue

			return redirect(r)

	else:
		recipe_form = RecipeForm(initial={'author': request.user.id})
		amount_formset = AmountFormSet(prefix='amount')
		step_formset = StepFormSet(prefix='step')

	return render(request, 'recipe/recipe_form.html',{
		'recipe_form': recipe_form,
		'amount_formset': amount_formset,
		'step_formset': step_formset,
		'Courses': RecipeCategory.objects.filter(parent__name='Courses').only('name'),
		'Cuisines': RecipeCategory.objects.filter(parent__name='Cuisines').only('name'),
		'Main_Ingredients': RecipeCategory.objects.filter(parent__name='Main Ingredients').only('name'),
		'Special_Diets': RecipeCategory.objects.filter(parent__name='Special Diets').only('name'),
		})

@login_required
def recipe_edit(request, pk):
	"""
	Page for edit a recipe
	"""    
	recipe = get_object_or_404(Recipe, pk = pk)
	if request.user != recipe.author:
		raise Http404
	AmountFormSet = formset_factory(AmountForm, extra = 1)
	StepFormSet = formset_factory(StepForm, extra = 1)
	if request.method == 'POST':
		recipe_form = RecipeForm(request.POST, instance = recipe)
		amount_formset = AmountFormSet(request.POST, prefix='amount')
		step_formset = StepFormSet(request.POST, prefix='step')
		if recipe_form.is_valid() and amount_formset.is_valid() and step_formset.is_valid():
			r = recipe_form.save()
			
			# Process step
			step = 0
			for form in step_formset:
				des = ''
				if 'description' in form.cleaned_data:
					des = form.cleaned_data['description']
				else:
					continue
				s, created = Step.objects.get_or_create(recipe = r, step_num= step, defaults={'description': des})
				s.description = des
				s.step_image = form.cleaned_data['step_image'];
				s.save()
				step = step + 1

			# Process amount
			unactive = get_object_or_404(FoodCategory, pk = 1)
			for form in amount_formset:
				if 'ingredient' in form.cleaned_data:
					f, created = Food.objects.get_or_create(name = form.cleaned_data['ingredient'], defaults={'category': unactive})
					a, created = Amount.objects.get_or_create(ingredient = f, recipe = r, defaults={'amount':form.cleaned_data['amount'], 'must':form.cleaned_data['must']})
					a.amount = form.cleaned_data['amount']
					a.must = form.cleaned_data['must']
					a.save()
				else:
					continue

			return redirect(r)


	else:
		""" Give initial data """
		recipe_form = RecipeForm(instance = recipe)

		amount = recipe.amount_set.all()
		initial_amount = []
		for a in amount:
			initial_amount.append({	'ingredient':a.ingredient,
									'amount': a.amount,
									'must': a.must,
									})

		step = recipe.step_set.all()
		initial_step = []
		for s in step:
			u = ''
			if s.step_image:
				u = s.step_image.url
			initial_step.append({	'description':s.description,
									'step_image':u
									})

		amount_formset = AmountFormSet(initial = initial_amount ,prefix='amount')
		step_formset = StepFormSet(initial = initial_step, prefix='step')

	return render(request, 'recipe/recipe_form.html',{
		'recipe_form': recipe_form,
		'amount_formset': amount_formset,
		'step_formset': step_formset,
		})

@login_required
def recipe_delete(request, pk):
	recipe = get_object_or_404(Recipe, pk = pk)
	name = recipe.name
	if recipe.author == request.user:
		recipe.amount_set.all().delete()
		recipe.step_set.all().delete()
		recipe.delete()
		action.send(request.user, verb="deleted recipe %s" % name)
		return render(request, 'recipe/recipe_delete.html', {'recipe': name,})

	else:
		raise Http404

@login_required
def did_recipe_upload(request, pk):
	recipe = get_object_or_404(Recipe, pk = pk)
	if request.method == 'POST':
		form = DidRecipeForm(request.POST, request.FILES)
		if form.is_valid():
			if request.user != form.cleaned_data['user']:
				raise Http404
			form.save()

		return redirect(recipe)
	else:
		form = DidRecipeForm(initial= {'recipe': recipe.id, 'user': request.user.id,})

	return render(request, 'recipe/did_form.html', {
			'form': form,
		})


def image_delete(request):
	if request.is_ajax() and request.method=='POST' and request.user.is_authenticated():
		f = request.POST.get('file')
		if f == '':
			return HttpResponse('fail')
		p = os.path.join(settings.SITE_ROOT,settings.MEDIA_ROOT,f)
		print >> sys.stderr, 'Delete Path: ', os.path.dirname(p)
		if os.path.exists(p):
			shutil.rmtree(os.path.dirname(p))
		return HttpResponse('success')
	else:
		raise Http404	





