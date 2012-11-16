from django.forms import ModelForm
from recipe.models import Recipe, Step, Vote
from django.forms.models import inlineformset_factory
from django import forms

class RecipeForm(ModelForm):
	prep_time = forms.TimeField(input_formats=['%H:%M',])
	cook_time = forms.TimeField(input_formats=['%H:%M',])
	class Meta:
		model = Recipe
		fields = ('name', 'author', 'category', 'brief', 'cover_image', 'tips', 'prep_time', 'cook_time')
		widgets = {
			'author': forms.HiddenInput(),
		}

class VoteForm(forms.Form):
	score = forms.IntegerField(min_value = 0, max_value = 5)
	comment = forms.CharField(widget=forms.Textarea)

class StepForm(forms.Form):
	description = forms.CharField(min_length = 1)
	step_image = forms.ImageField(required=False)

class AmountForm(forms.Form):
	ingredient = forms.CharField(min_length = 1)
	amount = forms.CharField(min_length = 1)
	must = forms.BooleanField()


