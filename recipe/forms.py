from django.forms import ModelForm
from recipe.models import Recipe, Step, Vote, DidRecipe
from django.forms.models import inlineformset_factory
from django import forms
from django.conf import settings
import os
import sys

class DidRecipeForm(ModelForm):
	class Meta:
		model = DidRecipe
		exclude = ('date', )
		widgets = {
			'recipe': forms.HiddenInput(),
			'user': forms.HiddenInput(),
		}

class RecipeForm(ModelForm):
	prep_time = forms.TimeField(input_formats=['%H:%M','%H:%M:%S',])
	cook_time = forms.TimeField(input_formats=['%H:%M','%H:%M:%S',])
	cover_image = forms.CharField(widget=forms.HiddenInput(), required=False)
	class Meta:
		model = Recipe
		fields = ('name', 'author', 'category', 'brief', 'cover_image', 'tips', 'prep_time', 'cook_time')
		widgets = {
			'author': forms.HiddenInput(),
		}

class VoteForm(forms.Form):
	score = forms.IntegerField(min_value = 0, max_value = 5)
	comment = forms.CharField(widget=forms.Textarea, required=False)

class StepForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(), min_length = 1)
	step_image = forms.CharField(widget=forms.HiddenInput(), required=False)

class AmountForm(forms.Form):
	ingredient = forms.CharField(min_length = 1)
	amount = forms.CharField(min_length = 1)
	must = forms.BooleanField(required=False)


