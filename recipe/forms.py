from django.forms import ModelForm
from recipe.models import Recipe

class RecipeForm(ModelForm):
	class Meta:
		model = Recipe
		exclude = {'date', 'author', 'did_num', 'like_num', 'view_num'}

