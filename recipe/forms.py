from django.forms import ModelForm
from recipe.models import Recipe, Step
from django.forms.models import inlineformset_factory


class RecipeForm(ModelForm):
	class Meta:
		model = Recipe
		exclude = {'date', 'author', 'did_num', 'like_num', 'view_num'}

RecipeStepFormSet = inlineformset_factory(Recipe, Step, extra = 5)
