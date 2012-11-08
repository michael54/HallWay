# Create your views here.
from django.shortcuts import render
from userena.views import signin
from django.views.generic.edit import CreateView
from recipe.models import Recipe
from recipe.forms import RecipeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

def nav(request):
	return render(request, 'nav.html')

def index(request):
	return render(request, 'recipe/index.html')

class RecipeCreate(CreateView):
	form_class = RecipeForm
	model = Recipe

	@method_decorator(login_required)

	def form_valid(self, form):
		form.instance.author = self.request.userena
		return super(RecipeCreate, self).form_valid(form)

class RecipeDetailView(DetailView):
	queryset = Recipe.objects.all()

	def get_object(self):
		object = super(RecipeDetailView, self).get_object();

		object.view_num = object.view_num + 1
		object.save()

		return object


