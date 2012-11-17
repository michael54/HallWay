# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from userena.views import signin
from django.views.generic.edit import CreateView
from recipe.models import Recipe, RecipeCategory, Vote, Step, Amount
from recipe.forms import RecipeForm, VoteForm, StepForm, AmountForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from recipe import recommendations, itemsim
from recipe.tasks import add_view_num, get_or_create_vote, add_like_num
from django.template import Context
from django.core.urlresolvers import reverse
from food.models import Food
from django.core import serializers
from actstream import actions, models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.forms.formsets import formset_factory
import sys 
from django.conf import settings
from ajaxuploader.views import AjaxFileUploader
from ajaxuploader.backends.easythumbnails import EasyThumbnailUploadBackend
import uuid

cover_image_upload = AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(540,000), QUALITY=90, UPLOAD_DIR='Recipe_Images/Cover_Images')

step_image_upload = AjaxFileUploader(backend=EasyThumbnailUploadBackend, DIMENSIONS=(160,000), QUALITY=75, UPLOAD_DIR='Recipe_Images/Step_Image')

def nav(request):
	return render(request, 'nav.html')

def index(request):
	if request.is_ajax():
		data = ''
		q = request.POST['q']
		queries = {}
		queries['recipe'] = Recipe.objects.filter(name__contains= q)[:3]
		queries['food'] = Food.objects.filter(name__contains=q)[:3]
		if queries['recipe']:
			data += '<span class="category">Recipe</span>'
			for obj in queries['recipe']:
				data+= '<a href="'+obj.get_absolute_url()+'">'
				data+= '<span class="searchheading">'+obj.name+'</span></a>'
				brief = obj.brief
				if len(brief) > 50:
					brief = brief[:50]
				data+= '<span>'+brief+'</span>'

		if queries['food']:
			data += '<span class="category">Food</span>'
			for obj in queries['food']:
				data+= '<a href="'+obj.get_absolute_url()+'">'
				data+= '<span class="searchheading">'+obj.name+'</span></a>'
				brief = obj.brief
				if len(brief) > 50:
					brief = brief[:50]
				data+= '<span>'+brief+'</span>'
		return HttpResponse(data)
	else:
		return render(request, 'recipe/index.html')

class RecipeDetailView(DetailView):
	queryset = Recipe.objects.all()

	def get_object(self):
		object = super(RecipeDetailView, self).get_object()

		add_view_num.delay(object)

		return object

	def get_context_data(self, **kwargs):
		context = super(RecipeDetailView, self).get_context_data(**kwargs)
		if str(context['object'].id) in itemsim.itemsim:
			id_list = []
			for (similarity, i) in itemsim.itemsim[str(context['object'].id)]:
				id_list.append(i)

			objects = Recipe.objects.filter(id__in=id_list)
			objects = dict([(obj.id, obj) for obj in objects])
			sorted_objects = [objects[id] for id in id_list]
			context['recommends'] = sorted_objects[0:10]

		if self.request.user.is_authenticated():
			try:
				vote = Vote.objects.get(recipe = context['object'], user=self.request.user)
			except Vote.DoesNotExist:
				context['vote'] = None
			else:
				context['vote'] = vote
		
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

@login_required
def like(request, pk):
	"""
	Handle ajax request to like a recipe from a user 
	"""
	if request.is_ajax():
		recipe = get_object_or_404(Recipe, pk=pk)
		profile = request.user.get_profile()
		profile.favourite_recipes.add(recipe)
		action.send(request.user, verb='liked', target = recipe)
		add_like_num.delay(recipe, 1)

		return HttpResponse('Liked')
	else:
		raise Http404	


@login_required
def unlike(request, pk):
	"""
	Handle ajax request to unlike a recipe from a user 
	"""
	if request.is_ajax():
		recipe = get_object_or_404(Recipe, pk=pk)
		profile = request.user.get_profile()
		profile.favourite_recipes.remove(recipe)
		action.send(request.user, verb='liked', target = recipe)
		add_like_num.delay(recipe, -1)

		return HttpResponse('Liked')
	else:
		raise Http404	




@login_required
def activity(request):
    """
    Index page for authenticated user's activity stream. 
    """
    return render(request, 'actstream/update.html', {
        'ctype': ContentType.objects.get_for_model(User),
        'actor': request.user, 'action_list': models.user_stream(request.user),
        'following': models.following(request.user),
        'followers': models.followers(request.user),
    })

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

			for form in amount_formset:
				if 'ingredient' in form.cleaned_data:
					f, created = Food.objects.get_or_create(name = form.cleaned_data['ingredient'], defaults={'category': 1})
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
		})

@login_required
def recipe_edit(request, pk):
	"""
	Page for edit a recipe
	"""    
	recipe = get_object_or_404(Recipe, pk = pk)
	AmountFormSet = formset_factory(AmountForm, extra = 1)
	StepFormSet = formset_factory(StepForm, extra = 1)
	if request.method == 'POST':
		recipe_form = RecipeForm(request.POST, request.FILES)
		amount_formset = AmountFormSet(request.POST, prefix='amount')
		step_formset = StepFormSet(request.POST, request.FILES, prefix='step')
		if recipe_form.is_valid() and amount_formset.is_valid() and step_formset.is_valid():
			r = recipe_form.save()
			step = 0
			for form in step_formset:
				des = ''
				if 'description' in form.cleaned_data:
					des = form.cleaned_data['description']
				else:
					continue
				img = 'step-'+str(step)+'-step_image'
				if img in request.FILES:
					s = Step(recipe = r, step_num = step, description = des, step_image = request.FILES[img])
				else:
					s = Step(recipe = r, step_num = step, description = des)
				s.save()
				step = step + 1

			for form in amount_formset:
				if 'ingredient' in form.cleaned_data:
					f, created = Food.objects.get_or_create(name = form.cleaned_data['ingredient'], defaults={'category': 1})
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
		})
