from django.forms import ModelForm
from recipe.models import Recipe, Step, Vote
from django.forms.models import inlineformset_factory
from django import forms

class RecipeForm(ModelForm):
	class Meta:
		model = Recipe
		exclude = {'date', 'author', 'did_num', 'like_num', 'view_num'}

RecipeStepFormSet = inlineformset_factory(Recipe, Step, extra = 5)

class VoteForm(forms.Form):
	score = forms.IntegerField(min_value = 0, max_value = 5)
	comment = forms.CharField()

	
