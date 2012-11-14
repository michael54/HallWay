# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from userena.views import signin
from django.views.generic.edit import CreateView
from recipe.models import Recipe, RecipeCategory, Vote
from recipe.forms import RecipeForm, RecipeStepFormSet, VoteForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from recipe import recommendations, itemsim
from recipe.tasks import add_view_num, get_or_create_vote
from django.template import Context
from django.core.urlresolvers import reverse

def nav(request):
	return render(request, 'nav.html')

def index(request):
	c = Context({'results': Recipe.objects.all() })
	return render(request, 'recipe/index.html', c)

class RecipeCreate(CreateView):
	form_class = RecipeForm
	model = Recipe
	success_url = 'thanks/'
	
	@method_decorator(login_required)
	def form_valid(self, form):
		context = self.get_context_data()
		form.instance.author = self.request.userena
		step_form = context['step_form']
		if step_form.is_valid():
			self.object = form.save()
			step_form.instance = self.object
			step_form.save()
			return HttpResponseRedirect('thanks/')
		else:
			return self.render(self.request, self.get_context_data(form=form))

	def form_invaild(self, form):
		return self.render(self.request, self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(RecipeCreate, self).get_context_data(**kwargs)
		if self.request.POST:
			context['step_form'] = RecipeStepFormSet(self.request.POST)
		else:
			context['step_form'] = RecipeStepFormSet()
		return context


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
			context['form'] = VoteForm
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
	# context_object_name = "hot_recipe_list"
	paginate_by = 10

def rate(request, pk):
	if request.method =="POST":
		recipe_object = Recipe.objects.get(pk = pk)
		user_object = request.user
		s = int(request.POST['score'])
		try:	
			v = Vote.objects.get(recipe = recipe_object, user = user_object)
		
		except Vote.DoesNotExist:
			v = Vote(recipe = recipe_object, user = user_object, score = s)
			
			recipe_object.cumulative_score = recipe_object.cumulative_score + s
			recipe_object.rating_num = recipe_object.rating_num + 1
			recipe_object.save()
			v.save()
		else:
			old_score = v.score
			v.score = s
			recipe_object.cumulative_score = recipe_object.cumulative_score + s - old_score
			recipe_object.save()
			v.save()
	else:
		raise Http404
	return HttpResponseRedirect(reverse('recipe_detail', args=(pk,)))



